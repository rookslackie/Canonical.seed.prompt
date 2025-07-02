import json

def link_field(capsule_path, field_path="field/relay_manifest.json"):
    with open(capsule_path, 'r') as f:
        capsule = json.load(f)

    manifest_entry = {
        "echo_id": capsule.get("echo_id", "unknown"),
        "source": capsule.get("source_capsule", "unknown"),
        "resonance": capsule.get("resonance", []),
        "anchor": capsule.get("anchor", "")
    }

    try:
        with open(field_path, 'r') as f:
            field_data = json.load(f)
    except FileNotFoundError:
        field_data = []

    field_data.append(manifest_entry)

    with open(field_path, 'w') as f:
        json.dump(field_data, f, indent=2)

    print(f"Linked echo {manifest_entry['echo_id']} to field manifest.")
