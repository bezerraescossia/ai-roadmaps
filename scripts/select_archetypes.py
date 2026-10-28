# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Turn interview 1 answers (the shape of the project) into a primary archetype plus included ones.

Usage:
  uv run scripts/select_archetypes.py --answers '{"purpose": "product", "runtime": "interactive-service",
                                                   "own_models": ["tabular-or-time-series"]}'

Prints JSON: primary, includes, unsupported, reasons, needs. See archetypes/_selection.md.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan as planner  # noqa: E402

RUNTIME = {"interactive-service": "llm-service", "agent": "agent", "batch-pipeline": "batch-pipeline"}
MODELS = {"tabular-or-time-series": "classical-ml", "images-video-audio": "perception",
          "llm-adaptation": "fine-tuning"}


def select(answers: dict) -> dict:
    result = {"primary": None, "includes": [], "unsupported": [], "reasons": [], "needs": []}
    purpose = answers.get("purpose")
    runtime = answers.get("runtime")
    models = [m for m in answers.get("own_models") or [] if m != "none"]
    unknown = [m for m in models if m not in MODELS]
    if unknown:
        sys.exit(f"unknown own_models value(s): {unknown}; choose from {sorted(MODELS)}")

    if purpose == "feasibility-study":
        result["primary"] = "poc"
        result["reasons"].append("A feasibility study is a timeboxed spike; its last spec recommends the "
                                 "archetype for the production roadmap.")
        return result
    if purpose == "platform":
        result["primary"] = "ml-platform"
        result["reasons"].append("The product is the shared platform; the models built on it are its users.")
        return result
    if purpose != "product":
        result["needs"].append("purpose")
        return result

    if runtime in RUNTIME:
        result["primary"] = RUNTIME[runtime]
        result["reasons"].append(f"`{runtime}` describes how the system runs.")
        declared = planner.load_archetype(result["primary"]).get("includes", {})
        for kind in models:
            archetype = MODELS[kind]
            if archetype in declared:
                result["includes"].append(archetype)
                result["reasons"].append(f"You train or adapt a model ({kind}), so `{archetype}` is included.")
            else:
                result["unsupported"].append({"archetype": archetype,
                                              "reason": f"{result['primary']} does not include it; use a separate project."})
    elif runtime == "model-only":
        if not models:
            result["needs"].append("own_models")
            return result
        result["primary"] = MODELS[models[0]]
        result["reasons"].append(f"The product is a trained model ({models[0]}).")
        for kind in models[1:]:
            result["unsupported"].append({"archetype": MODELS[kind],
                                          "reason": "model-building archetypes cannot include each other; "
                                                    "use a separate project for this model."})
    else:
        result["needs"].append("runtime")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--answers", required=True, help="JSON object of interview 1 answers")
    print(json.dumps(select(json.loads(parser.parse_args().answers)), indent=2))
