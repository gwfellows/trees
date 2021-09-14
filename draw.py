import webbrowser
import svgwrite
import time


def draw(leaf_positions, branch_positions, score, sx=0, sy=300, r=2):
    dwg = svgwrite.Drawing(
        "_".join((str(score), time.strftime("%Y%m%d-%H%M%S"))) + ".svg",
        viewBox="-400 -400 800 400",
    )
    for x, y in leaf_positions:
        dwg.add(
            dwg.circle(
                center=(x, -y),
                r=r,
                stroke=svgwrite.rgb(0, 255, 0),
                fill=svgwrite.rgb(0, 255, 0),
            )
        )
    for x1, y1, x2, y2 in branch_positions:
        dwg.add(dwg.line((x1, -y1), (x2, -y2), stroke=svgwrite.rgb(139, 69, 19)))
    dwg.add(
        dwg.circle(
            center=(sx, -sy),
            r=10,
            stroke=svgwrite.rgb(255, 255, 0),
            fill=svgwrite.rgb(255, 255, 0),
        )
    )
    dwg.save()