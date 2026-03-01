import logging
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)


def record(portal_url: str, output_path: str) -> None:
    """Launch Playwright codegen to record login steps against the portal."""
    output = Path(output_path)

    print(
        "\n"
        "=== Sophos Login Recorder ===\n"
        "\n"
        "A browser will open. Perform the login steps on the portal.\n"
        "Use  __USERNAME__  as the username and  __PASSWORD__  as the password.\n"
        "Close the browser when done. The script will be saved automatically.\n"
    )

    cmd = [
        sys.executable,
        "-m",
        "playwright",
        "codegen",
        "--target",
        "python",
        "-o",
        str(output),
        portal_url,
    ]
    log.info("Launching: %s", " ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"Playwright codegen failed (exit code {exc.returncode})")
    except FileNotFoundError:
        raise SystemExit(
            "Playwright not found. Install it with: pip install playwright && playwright install chromium"
        )

    if not output.exists():
        raise SystemExit(
            f"Recording was not saved to {output}. "
            "Make sure you performed actions in the browser before closing it."
        )

    script_text = output.read_text()
    has_username = "__USERNAME__" in script_text
    has_password = "__PASSWORD__" in script_text

    if not has_username or not has_password:
        missing = []
        if not has_username:
            missing.append("__USERNAME__")
        if not has_password:
            missing.append("__PASSWORD__")
        log.warning(
            "Recorded script is missing placeholders: %s. "
            "Credential substitution may not work correctly. "
            "Consider re-recording and using the exact placeholder strings.",
            ", ".join(missing),
        )
    else:
        log.info("Recording saved to %s with both placeholders found.", output)

    print(f"\nRecorded script saved to: {output}")
