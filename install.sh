#!/usr/bin/env bash
set -euo pipefail

REPO="marketingskills/seo"
INSTALL_DIR="${HOME}/.seo-agency"

echo "==> Installing SEO Operator skills from ${REPO}..."
echo "    Target: ${INSTALL_DIR}"
echo ""

if [ -d "${INSTALL_DIR}/.git" ]; then
    echo "==> Updating existing install..."
    git -C "${INSTALL_DIR}" pull --ff-only
    exit 0
fi

echo "==> Cloning repository..."
git clone --depth=1 "https://github.com/${REPO}.git" "${INSTALL_DIR}" 2>/dev/null || {
    echo "==> Downloading latest release..."
    mkdir -p "${INSTALL_DIR}"
    curl -fsSL "https://github.com/${REPO}/archive/main.tar.gz" | tar -xz -C "${INSTALL_DIR}" --strip-components=1
}

SKILL_COUNT=$(find "${INSTALL_DIR}/skills" -maxdepth 1 -mindepth 1 -type d | wc -l)
echo ""
echo "==> Installed ${SKILL_COUNT} skills to ${INSTALL_DIR}/skills/"
echo ""
echo "    To activate, ask your agent:"
echo '    "help me use the SEO skills installed at '"${INSTALL_DIR}/skills"'"'
echo ""
echo "    Or load a specific skill:"
echo "    Load the traffic-decay-detector skill from ${INSTALL_DIR}/skills/traffic-decay-detector/SKILL.md"
echo ""
echo "    For live GSC/GA4 data, load:"
echo "    ${INSTALL_DIR}/skills/live-search-console-data/SKILL.md"
