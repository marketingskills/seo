#!/usr/bin/env bash
set -euo pipefail

runtime="${SEO_LOOP_RUNTIME:-codex}"
mode="${SEO_LOOP_MODE:-report-only}"
timeout_limit="${SEO_LOOP_TIMEOUT:-3h}"
kill_after="${SEO_LOOP_KILL_AFTER:-5m}"

if [[ -z "${SEO_LOOP_PROJECT_DIR:-}" ]]; then
  echo "SEO_LOOP_PROJECT_DIR is required" >&2
  exit 64
fi

project_dir="${SEO_LOOP_PROJECT_DIR}"
if [[ ! -d "${project_dir}" ]]; then
  echo "SEO_LOOP_PROJECT_DIR does not exist: ${project_dir}" >&2
  exit 66
fi

project_key="$(printf '%s' "${project_dir}" | tr -c 'A-Za-z0-9._-' '_')"
lock_file="${SEO_LOOP_LOCK_FILE:-/tmp/seo-growth-loop-${project_key}.lock}"
log_dir="${SEO_LOOP_LOG_DIR:-${project_dir}/seo-growth-logs}"

mkdir -p "${log_dir}"

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
log_file="${log_dir}/seo-growth-${timestamp}.log"
latest_file="${log_dir}/latest.log"

prompt="Use the seo-growth-loop skill. Run exactly one bounded SEO growth loop for this project in ${mode} mode.

Operating rules:
- Start with project preflight: infer framework, source of truth, existing SEO/growth commands, work logs, verification path, and indexing path.
- Prefer real GSC/analytics/search performance evidence when available.
- Infer whether this project publishes content from Git, a CMS/API, or a hybrid of code templates plus API content records before choosing the action.
- If the project already has a mature SEO/growth command or opportunity queue, use that as input instead of creating a parallel workflow.
- Choose one action or one reportable opportunity queue, then stop.
- Default to report-only behavior unless ${mode} explicitly allows publishing and the project configuration provides a safe publishing path.
- Do not start servers, app daemons, background workers, remote-control services, or long-lived sessions.
- Do not wait for interactive approval prompts.
- Write or update the configured SEO work log, include verification status, and finish."

case "${runtime}" in
  codex)
    agent_cmd=(codex exec --ephemeral --cd "${project_dir}" --ask-for-approval never "${prompt}")
    ;;
  opencode)
    agent_cmd=(opencode run --dir "${project_dir}" "${prompt}")
    ;;
  *)
    echo "Unsupported SEO_LOOP_RUNTIME: ${runtime}. Use codex or opencode." >&2
    exit 64
    ;;
esac

set +e
{
  echo "started_at=${timestamp}"
  echo "runtime=${runtime}"
  echo "mode=${mode}"
  echo "project_dir=${project_dir}"
  echo "lock_file=${lock_file}"
  echo "timeout=${timeout_limit}"
  echo

  exec 9>"${lock_file}"
  if ! flock -n 9; then
    echo "Another seo-growth-loop run is active; skipping this run."
    exit 0
  fi

  if command -v timeout >/dev/null 2>&1; then
    timeout --kill-after="${kill_after}" "${timeout_limit}" "${agent_cmd[@]}"
  else
    echo "GNU timeout is not available; running without a wall-clock timeout." >&2
    "${agent_cmd[@]}"
  fi
} 2>&1 | tee "${log_file}"
status="${PIPESTATUS[0]}"
set -e

cp "${log_file}" "${latest_file}"
exit "${status}"
