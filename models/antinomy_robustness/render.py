"""Render the factorial grid as compact, code-native SVG small multiples."""

from __future__ import annotations

from html import escape

from models.antinomy.sweep import REGIME_ORDER, ParameterGrid

from .experiment import ScenarioResult

COLORS = {
    "collapse": "#374151",
    "equilibrium": "#4f9c89",
    "lock-in": "#c77a42",
    "oscillation": "#7965a8",
    "unresolved": "#e8d86c",
}
PANEL_WIDTH = 300
PANEL_HEIGHT = 330


def render_panel(result: ScenarioResult, grid: ParameterGrid, index: int) -> str:
    """Draw one regime map with equal-sized grid cells and explicit axes."""
    column, row = index % 3, index // 3
    support_index = {
        value: position for position, value in enumerate(grid.shared_support_values)
    }
    inhibition_index = {
        value: position for position, value in enumerate(grid.cross_inhibition_values)
    }
    width = 230 / len(support_index)
    height = 240 / len(inhibition_index)
    paths: dict[str, list[str]] = {regime: [] for regime in REGIME_ORDER}
    for cell in result.cells:
        horizontal = 40 + support_index[cell.support] * width
        vertical = 275 - (inhibition_index[cell.inhibition] + 1) * height
        paths[cell.modal].append(
            f"M{horizontal:.3f},{vertical:.3f}h{width:.3f}v{height:.3f}h-{width:.3f}z"
        )
    heading = f"{result.scenario.response}, {result.scenario.schedule}"
    parts = [
        f'<g transform="translate({column * PANEL_WIDTH},{85 + row * PANEL_HEIGHT})">',
        f'<text x="40" y="14">{escape(heading)}</text>',
        '<text x="40" y="29">directional asymmetry: '
        f"{result.scenario.asymmetry:+.1f}</text>",
    ]
    parts.extend(
        f'<path fill="{COLORS[regime]}" d="{"".join(paths[regime])}"/>'
        for regime in REGIME_ORDER
    )
    parts.extend(
        [
            f'<text x="40" y="293">{grid.shared_support_values[0]:g}</text>',
            f'<text x="257" y="293">{grid.shared_support_values[-1]:g}</text>',
            '<text x="127" y="308">support</text>',
            f'<text x="20" y="275">{grid.cross_inhibition_values[0]:g}</text>',
            f'<text x="14" y="45">{grid.cross_inhibition_values[-1]:g}</text>',
            '<text transform="translate(12,205) rotate(-90)">inhibition</text>',
            "</g>",
        ]
    )
    return "\n".join(parts)


def render_maps(results: tuple[ScenarioResult, ...], grid: ParameterGrid) -> str:
    """Produce an overview of all scenarios and their operational labels."""
    height = 85 + ((len(results) + 2) // 3) * PANEL_HEIGHT
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" '
        f'viewBox="0 0 900 {height}">',
        "<title>Antinomy structural robustness: modal regimes</title>",
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<g font-family="sans-serif" font-size="12" fill="#202733">',
        '<text x="30" y="25" font-size="19">Structural robustness: '
        "18 prespecified scenarios</text>",
        '<text x="30" y="46">Modal seed labels; classifier boundaries '
        "are not bifurcation proofs.</text>",
    ]
    for index, regime in enumerate(REGIME_ORDER):
        position = 30 + index * 165
        parts.append(
            f'<rect x="{position}" y="60" width="13" height="13" '
            f'fill="{COLORS[regime]}"/>'
            f'<text x="{position + 20}" y="71">{regime}</text>'
        )
    parts.extend(
        render_panel(result, grid, index) for index, result in enumerate(results)
    )
    return "\n".join([*parts, "</g></svg>", ""])
