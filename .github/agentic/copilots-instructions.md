# Copilot Instructions – gold-core-datamart-dbt

## Project overview

dbt project (project name: `insight_core`) that transforms raw Decathlon data into analytics-ready models on Databricks/Delta Lake. SQL dialect is **Databricks SQL**. Models are organized in three layers: **staging → intermediate → marts**.

## Your role

Act as a senior analytics engineer with expertise in dbt, Databricks SQL, data modeling and software engineering best practices. Your task is to assist in writing new models, refactoring existing models, and ensuring adherence to project conventions and architecture. You will also help with documentation and testing strategies to maintain high data quality standards.

## Commands

```bash
# First-time setup
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Install / reset
dbt deps                                  # Install packages (required after packages.yml changes)
dbt clean && dbt deps && dbt parse        # Full reset

# Validate a single model (no execution)
dbt compile --select <model_name>

# Preview results (runs but doesn't materialize)
dbt show --select <model_name>

# Run + test a single model
dbt build --select <model_name>

# Run tests only (single model)
dbt test --select <model_name>

# Run tests by tag
dbt test --select tag:alerting            # Core functional/quality checks
dbt test --select tag:analytic            # Deep debugging checks (run after alerting failures)

# Lint SQL
sqlfluff fix models/path/to/model.sql     # Auto-fix SQL style
sqlfluff lint models/path/to/model.sql    # Check only

# Validate model metadata
dbt-score lint --model <model_name>       # Check 20+ metadata requirements
dbt-score list                            # List all scoring rules
```

**Default safe target**: `dev`. Never run against `preprod` or `prod` without explicit approval.

## Architecture

### Layer materializations

| Layer | Path | Materialization | Notes |
|---|---|---|---|
| `staging` | `models/staging/` | ephemeral | Thin wrappers over sources; minimal transformation |
| `intermediate` | `models/intermediate/` | ephemeral | Business logic, joins, calculations |
| `marts` | `models/marts/` | table (Delta) | End-user datasets; include `dim_*`, `sales`, `stock`, `price`, etc. |
| `active_schema` | `models/active_schema/` | table (Delta) | Operational views |

Staging sources are organized by source system (e.g., `datalake_silver`, `datalake_gold_sales`, `datalake_gold_customer_360`). Intermediate models are organized by business domain (e.g., `sales/`, `stock/`, `member/`, `shortage/`). Marts are organized under `dim/`, `sales/`, `stock/`, `price/`, `marketplace/`, `discount/`.

### Key packages (packages.yml)

- `dbt_utils` – surrogate keys, tests, macros
- `dbt_expectations` – column-level data quality tests
- `dbt_date` – date utilities (`dbt_date.now()`)
- `dbt_artifacts` – uploads run results to monitoring schema (preprod/prod only)
- `audit_helper` – compare queries/relations for refactoring validation

## Key conventions

### Every model must end with `{{ ROW_LIMIT_FOR_CI() }}`

```sql
select ...
from ...
{{ ROW_LIMIT_FOR_CI() }}
```

This macro applies `LIMIT 100` on `ci` targets and when `is_slim_run=true` on dev. Omitting it causes full table scans during CI.

### Staging model pattern

```sql
select column_1,
       column_2,
       ...
from 
  {{ source('source_name', 'table_name') }}

{{ ROW_LIMIT_FOR_CI() }}
```

- No business logic nor only renaming/casting in staging models — those belong in intermediate layer
- Commas are **trailing** (after each item in a list), not leading

### SQL style (enforced by SQLFluff / Databricks dialect)

- Keywords: `lower` (`select`, `from`, `where`, `left join`, `with`, `as`, etc.)
- Identifiers/aliases: `lower_snake_case`
- Functions: `lower` (`coalesce`, `cast`, `date_add`, `row_number`)
- Indentation: 4 spaces
- Commas: trailing position (after each item in a list)
- Subqueries in `from`/`where` are forbidden — use CTEs instead - in other words, **no nested queries**
- Explicit column aliases required (no implicit aliasing)
- Single quotes for string literals
- No trailing semicolons
- Max line length: 80 chars (long lines use `--noqa` inline comment to suppress)
- JOINs must be fully qualified (`inner join`, not just `join`)
- CTEs must be lowercased (`with`/`as`), and each CTE must be separated by a blank line for readability
- No `select *` (explicitly list columns)
- Use `group by all` instead of `group by` when grouping by all selected columns
- Use `cast(column as type)` instead of `column::type` for readability and compatibility
- Use `coalesce(column, default)` instead of `ifnull` or `nvl` for null handling
- Use `date_add('day', 1, date_column)` instead of `date_column + interval '1 day'` for date arithmetic
- Use `{{ ref('model_name') }}` for referencing other models, never hardcoded table names
- Use `{{ source('source_name', 'table_name') }}` for referencing raw sources
- Use `{{ var('variable_name') }}` for referencing variables defined in `dbt_project.yml` or passed via CLI

### Primary keys

Use `dbt_utils.generate_surrogate_key()`:

```sql
{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }} AS <model_name>_id
```

### YAML config structure

Each model has a paired `.yml` file. Mart models require:

```yaml
version: 2
models:
  - name: <model_name>
    description: "{{ doc('business_<model_name>') }}"
    meta:
      contains_pii: false
      owner:
        support_group: "CE-CORE-DATAMART"
        email: "cecoredatamart@decathlon.net"
        github_repo: "https://github.com/dktunited/insight-core-datamart-dbt"
        dbt_documentation: "https://symmetrical-fishstick-4gwqqrn.pages.github.io/"
    columns:
      - name: <column>
        data_type: <type>
        description: "..."
        meta:
          primary_key: true
        data_tests:
          - unique:
              config: { tags: [alerting] }
          - not_null:
              config: { tags: [alerting] }
```

Staging models require `description` + `data_type` per column, but don't need `meta.owner` or `airflow` blocks. Use `meta.exclude_from_ci: true` to skip a staging model in CI.

### Test tagging strategy

Tests must be tagged to one of three tiers:

| Tag | Purpose | When run |
|---|---|---|
| `ci` | Structural checks (`expect_column_to_exist`) | Every PR in CI |
| `alerting` | Core quality checks (`unique`, `not_null`, `at_least_one`) | After every prod run |
| `analytic` | Deep diagnostic checks | Only if `alerting` fails |


### Documentation

Each model has **two** paired `.md` doc files, stored in a `docs/` subfolder alongside the model:

| File | Doc block name | Referenced from |
|---|---|---|
| `business_<model_name>.md` | `business_<model_name>` | `.yml` `description` field |
| `technical_<model_name>.md` | `technical_<model_name>` | linked from business doc |

**Naming convention** (single underscore, no double underscore):

```yaml
description: "{{ doc('business_<model_name>') }}"
```

**Templates** — always use the canonical templates as a starting point:

- Business doc: `docs/guides/dbt-docs/business_doc_template.md`
- Technical doc: `docs/guides/dbt-docs/technical_doc_template.md`

The templates contain HTML comments (`<!-- ... -->`) that act as AI agent instructions; these are stripped by dbt at render time and must not be removed.

- When adding a new doc page, update `mkdocs.yml` navigation
- Style guides: `docs/style-guides/documentation-guide.md` and `docs/style-guides/yaml-configuration-guide.md`

### Custom tests

Custom test SQL files live in `tests/generic/`. Each test should have a folder with `.sql`, `.yml`, and `.md` docblock.

### Variables

Key project-level variables (set in `dbt_project.yml`, override with `--vars`):

- `is_slim_run` – activates row limiting on dev
- `param_country` – country filter (default: `GB`)
- `nb_month_history` – lookback period (default: 48 months)
- `fedid` – user federated ID for schema isolation on dev

### Schema naming

`generate_schema_name` is overridden — schemas come directly from `custom_schema_name` (no `target.schema` prefix). Target-to-schema mappings are defined per domain variable in `dbt_project.yml`.

## Agentic skills process

Local skills live under `.github/agentic/skills/**`.

### Skills-first enforcement (mandatory, all skills)
- For any request covered by a local skill in `.github/agentic/skills/**`, follow the skill workflow first, before using direct MCP, terminal, or ad-hoc actions.
- If runtime skill discovery does not expose the skill, load its local `SKILL.md` manually and apply its **Required Behavior**, **Workflow**, and **Review Checks** sections.
- If a skill script/tool dependency is missing (for example `uv`), stop and ask the user for fallback approval; do not skip directly to ad-hoc drafting.
- In final responses for skill-driven tasks, state whether execution was via runtime skill loading or local `SKILL.md` fallback.

### Pull request authoring workflow
- Use the live skill at `.github/agentic/skills/github/pull-request-authoring-workflow/SKILL.md` for pull request work.
- **Mandatory trigger**: when the user asks to open/create/update a PR (or asks PR title/body/help), load and follow `pull-request-authoring-workflow` before using direct GitHub MCP PR actions.
- Draft PR titles and bodies locally from the branch, diff, and `.github/pull_request_template.md`.
- Use `.github/agentic/skills/github/pull-request-authoring-workflow/scripts/draft_pr.py` to bootstrap PR drafts.
- Use the GitHub MCP only for GitHub-side PR actions such as creating or updating the pull request.
- Keep checklist items unchecked, link related tickets, and never include secrets or hardcoded credentials.
- Before creating a PR, check whether an open PR already exists for the current head branch and update it instead of creating a duplicate.
- Never call GitHub MCP PR write actions until title/body are drafted from the skill process (script or approved fallback).
- If the skill or its scripts are unavailable, stop and ask the user how to proceed; do not silently bypass the process.

### Commit message guidelines
- Use the live skill at `.github/agentic/skills/github/commit-message-guidelines/SKILL.md` for commit message work.
- **Mandatory trigger**: when the user asks to write/suggest/fix a commit message, load and follow `commit-message-guidelines` before drafting.
- Review `git diff --staged` before drafting the message.
- Draft commit messages locally and use `.github/agentic/skills/github/commit-message-guidelines/scripts/suggest_commit_message.py` to bootstrap them.
- Use the conventional commit format `<type>(<scope>): <description>` with an imperative summary.
- Use the GitHub MCP only for GitHub-side repository actions, not for plain commit-message drafting.
- Base the message only on staged changes; do not infer scope from unstaged/untracked files.
- If nothing is staged, stop and ask the user whether to stage changes first; do not guess a message.
- Never draft a commit message before reviewing `git diff --staged` and applying the skill’s type/scope rules.
- If the skill or its scripts are unavailable, stop and ask the user how to proceed; do not silently bypass the process.

## CI/CD

- PRs trigger `ci-on-pr.yml`: slim run using `state:modified+` against the last manifest, target = `ci`
- SQL linting runs on every PR touching `models/**/*.sql` (auto-fix + comment)
- Merges to `main` trigger `ci-on-main.yml` (preprod deploy)
- Production deploys via tagged releases (see `docs/guides/hotfix.md` for hotfix procedure)
- `dbt_artifacts` uploads run results to monitoring schema on preprod/prod only

## Related resources

- MCP servers repo: https://github.com/dktunited/unified-analytics-mcp-servers
- MCP tools available: `generate_model_yaml_tool`, `lint_sql_model_tool`, `score_dbt_model_tool`, `execute_databricks_sql_query`
- dbt docs (hosted): https://symmetrical-fishstick-4gwqqrn.pages.github.io/
