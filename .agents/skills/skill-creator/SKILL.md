---
name: skill-creator
description: Project-local skill creation/update guide. Use when adding or updating skills under .agents/skills so GitHub collaborators get the same SRAD workflow skills.
---

# Skill Creator

Create skills under `.agents/skills/<skill-name>/`.

Required:

- `SKILL.md` with YAML frontmatter `name` and `description`.
- Concise body with only operational instructions.
- Optional `agents/openai.yaml` for UI metadata.

Validate with:

```bash
python scripts/validate_project_skills.py
```

Do not rely on global user skill paths for repository workflows. If a workflow matters for collaborators, commit a project-local skill copy.
