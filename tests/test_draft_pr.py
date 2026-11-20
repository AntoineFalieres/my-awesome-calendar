import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFT_PR_PATH = REPO_ROOT / ".github" / "skills" / "github" / "pull-request-authoring-workflow" / "scripts" / "draft_pr.py"
SPEC = importlib.util.spec_from_file_location("draft_pr", DRAFT_PR_PATH)
draft_pr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(draft_pr)


class DraftPullRequestTests(unittest.TestCase):
    def test_title_uses_inferred_scope(self):
        self.assertEqual(
            draft_pr.build_title("feat", "add calendars", "calendar"),
            "feat(calendar): add calendars",
        )

    def test_rendered_body_does_not_add_ticket_or_issue_reference(self):
        template = (
            "[Provide a brief description of what this PR achieves. Explain the problem it solves or the feature it adds.]\n"
            "[Fill this section only when the PR impacts a column schema: column removal, column creation, column addition, or column type change. Otherwise leave `No breaking changes`.]\n"
            "[List the specific changes you've made in this PR. Be detailed, especially if your PR includes multiple changes.]"
        )

        body = draft_pr.render_body(
            template=template,
            description="Add calendar support.",
            breaking_changes="No breaking changes",
            changes_made="- Update `app.py`",
        )

        self.assertEqual(body, "Add calendar support.\nNo breaking changes\n- Update `app.py`")
        self.assertNotIn("issue", body.lower())
        self.assertNotIn("ticket", body.lower())


if __name__ == "__main__":
    unittest.main()
