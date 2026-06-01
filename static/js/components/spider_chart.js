/**
 * Spider/Radar chart untuk visualisasi CPL.
 * Pure Canvas API, tanpa library eksternal.
 */
var SpiderChart = (function () {

    function draw(canvasId, dataPoints, maxValue) {
        maxValue = maxValue || 100;
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;

        var ctx = canvas.getContext("2d");
        var size = Math.min(canvas.width, canvas.height);
        var cx = canvas.width / 2;
        var cy = canvas.height / 2;
        var radius = size * 0.38;
        var n = dataPoints.length;
        var step = (2 * Math.PI) / n;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Grid rings
        var rings = [0.2, 0.4, 0.6, 0.8, 1.0];
        ctx.strokeStyle = "hsl(214, 20%, 89%)";
        ctx.lineWidth = 0.5;

        for (var ri = 0; ri < rings.length; ri++) {
            var r = radius * rings[ri];
            ctx.beginPath();
            for (var i = 0; i <= n; i++) {
                var angle = (i % n) * step - Math.PI / 2;
                var x = cx + r * Math.cos(angle);
                var y = cy + r * Math.sin(angle);
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.stroke();
        }

        // Axis lines
        ctx.strokeStyle = "hsl(214, 20%, 85%)";
        ctx.lineWidth = 0.5;
        for (var a = 0; a < n; a++) {
            var angle = a * step - Math.PI / 2;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + radius * Math.cos(angle), cy + radius * Math.sin(angle));
            ctx.stroke();
        }

        // Data polygon
        ctx.fillStyle = "hsla(211, 61%, 50%, 0.2)";
        ctx.strokeStyle = "hsl(211, 61%, 50%)";
        ctx.lineWidth = 2;
        ctx.beginPath();

        for (var d = 0; d <= n; d++) {
            var idx = d % n;
            var val = dataPoints[idx].value / maxValue;
            var ang = idx * step - Math.PI / 2;
            var px = cx + radius * val * Math.cos(ang);
            var py = cy + radius * val * Math.sin(ang);
            if (d === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }

        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Data points
        for (var p = 0; p < n; p++) {
            var v = dataPoints[p].value / maxValue;
            var pAngle = p * step - Math.PI / 2;
            var dotX = cx + radius * v * Math.cos(pAngle);
            var dotY = cy + radius * v * Math.sin(pAngle);

            ctx.beginPath();
            ctx.arc(dotX, dotY, 4, 0, 2 * Math.PI);
            ctx.fillStyle = "hsl(211, 61%, 50%)";
            ctx.fill();
        }

        // Labels
        ctx.fillStyle = "hsl(220, 26%, 14%)";
        ctx.font = "12px Inter, sans-serif";
        ctx.textAlign = "center";

        for (var l = 0; l < n; l++) {
            var lAngle = l * step - Math.PI / 2;
            var lx = cx + (radius + 24) * Math.cos(lAngle);
            var ly = cy + (radius + 24) * Math.sin(lAngle);
            var label = dataPoints[l].label;
            var score = Math.round(dataPoints[l].value);
            ctx.fillText(label + " (" + score + ")", lx, ly + 4);
        }
    }

    return { draw: draw };

})();
