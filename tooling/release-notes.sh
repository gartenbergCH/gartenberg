#!/usr/bin/env bash
#
# Erzeugt Release-Notes aus den Conventional Commits seit dem letzten Release.
#
# Verwendung:
#   tooling/release-notes.sh [<vorheriger-tag>] [<bis-ref>]
#
# Ohne Argumente wird der letzte von HEAD aus erreichbare v*-Tag als Startpunkt
# genommen und bis HEAD ausgewertet. Die Notes werden nach stdout geschrieben.
set -euo pipefail

from="${1:-}"
to="${2:-HEAD}"

if [ -z "$from" ]; then
    from="$(git describe --tags --abbrev=0 --match 'v*' "$to" 2>/dev/null || true)"
fi

if [ -n "$from" ]; then
    range="${from}..${to}"
else
    # Noch kein Release: alles seit dem ersten Commit.
    range="$to"
fi

# Abschnitte in Ausgabereihenfolge: Schluessel -> Ueberschrift
section_keys=(breaking feat fix perf refactor docs test build ci other)
declare -A section_titles=(
    [breaking]='⚠️ Breaking Changes'
    [feat]='Neue Funktionen'
    [fix]='Fehlerbehebungen'
    [perf]='Performance'
    [refactor]='Refactorings'
    [docs]='Dokumentation'
    [test]='Tests'
    [build]='Build & Abhängigkeiten'
    [ci]='CI'
    [other]='Sonstiges'
)
declare -A sections=()

add_entry() {
    local key="$1" entry="$2"
    sections[$key]+="${entry}"$'\n'
}

while IFS= read -r -d $'\x1e' commit; do
    # git log trennt die Records zusaetzlich mit einem Zeilenumbruch.
    commit="${commit#$'\n'}"
    [ -n "$commit" ] || continue
    sha="${commit%%$'\x1f'*}"
    rest="${commit#*$'\x1f'}"
    subject="${rest%%$'\x1f'*}"
    body="${rest#*$'\x1f'}"

    short="${sha:0:7}"
    key='other'
    scope=''
    description="$subject"
    breaking=0

    if [[ "$subject" =~ ^([a-zA-Z]+)(\(([^\)]*)\))?(!)?:[[:space:]]*(.+)$ ]]; then
        type="${BASH_REMATCH[1],,}"
        scope="${BASH_REMATCH[3]}"
        [ -n "${BASH_REMATCH[4]}" ] && breaking=1
        description="${BASH_REMATCH[5]}"
        case "$type" in
            feat|fix|perf|refactor|docs|test|ci) key="$type" ;;
            build|deps) key='build' ;;
            *) key='other' ;;
        esac
    elif [[ "$subject" =~ ^Bump[[:space:]] ]]; then
        # Dependabot-Commits vor der Umstellung auf Conventional Commits.
        key='build'
    fi

    if [[ "$body" == *'BREAKING CHANGE'* ]]; then
        breaking=1
    fi

    entry="- "
    [ -n "$scope" ] && entry+="**${scope}**: "
    entry+="${description} (${short})"

    if [ "$breaking" -eq 1 ]; then
        add_entry breaking "$entry"
    else
        add_entry "$key" "$entry"
    fi
done < <(git log --no-merges --reverse --pretty=format:'%H%x1f%s%x1f%b%x1e' "$range")

output=''
for key in "${section_keys[@]}"; do
    [ -n "${sections[$key]:-}" ] || continue
    output+="## ${section_titles[$key]}"$'\n\n'
    output+="${sections[$key]}"$'\n'
done

if [ -z "$output" ]; then
    output="Keine Änderungen seit ${from:-dem ersten Commit}."$'\n'
fi

printf '%s' "$output"
