#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-magzines_repo}"
REPOSITORY="${2:-${GITHUB_REPOSITORY:-}}"
DRY_RUN="${3:-true}"

if [[ -z "$REPOSITORY" ]]; then
  echo "Repository is required (for example: owner/repo)."
  exit 1
fi

SEEN="|"
ISSUE_COUNT=0

while IFS= read -r -d '' asset; do
  issue_dir=$(dirname "$asset")
  if [[ "$SEEN" == *"|$issue_dir|"* ]]; then
    continue
  fi
  SEEN="${SEEN}${issue_dir}|"
  ISSUE_COUNT=$((ISSUE_COUNT + 1))

  relative=${issue_dir#"$SOURCE_DIR"/}
  magazine_folder=${relative%%/*}
  issue_date=$(basename "$issue_dir" | tr -cd '0-9')
  case "$magazine_folder" in
    the_economist)
      mag_id="te"
      mag_name="The Economist"
      ;;
    the_new_yorker)
      mag_id="ny"
      mag_name="The New Yorker Magazine"
      ;;
    time_magzine)
      mag_id="tm"
      mag_name="TIME Magazine"
      ;;
    *)
      mag_id=""
      mag_name=""
      ;;
  esac

  if [[ -z "$mag_id" || ! "$issue_date" =~ ^[0-9]{8}$ ]]; then
    echo "Skipping unrecognized issue directory: $relative"
    continue
  fi

  shopt -s nullglob
  assets=("$issue_dir"/*.pdf "$issue_dir"/*.epub)
  shopt -u nullglob
  if [[ "${#assets[@]}" -eq 0 ]]; then
    continue
  fi

  tag="$mag_id-$issue_date"
  echo "$tag: ${#assets[@]} asset(s) from $relative"
  if [[ "$DRY_RUN" == "true" ]]; then
    continue
  fi

  staging_dir=$(mktemp -d)
  safe_mag_name=$(printf '%s' "$mag_name" | tr ' ' '-')
  for source_asset in "${assets[@]}"; do
    extension=${source_asset##*.}
    cp "$source_asset" "$staging_dir/$issue_date-$safe_mag_name.$extension"
  done
  shopt -s nullglob
  release_assets=("$staging_dir"/*.pdf "$staging_dir"/*.epub)
  shopt -u nullglob

  if gh release view "$tag" --repo "$REPOSITORY" >/dev/null 2>&1; then
    gh release view "$tag" \
      --repo "$REPOSITORY" \
      --json assets \
      --jq '.assets[].name' | while IFS= read -r existing_asset; do
        gh release delete-asset "$tag" "$existing_asset" \
          --repo "$REPOSITORY" \
          --yes
      done
    gh release upload "$tag" "${release_assets[@]}" --repo "$REPOSITORY" --clobber
  else
    gh release create "$tag" "${release_assets[@]}" \
      --repo "$REPOSITORY" \
      --target main \
      --title "$mag_name - $issue_date" \
      --notes "Migrated from the legacy magzines branch."
  fi
  rm -rf "$staging_dir"
done < <(find "$SOURCE_DIR" -type f \( -name '*.pdf' -o -name '*.epub' \) -print0)

echo "Migration scan complete. Issues found: $ISSUE_COUNT. Dry run: $DRY_RUN"
