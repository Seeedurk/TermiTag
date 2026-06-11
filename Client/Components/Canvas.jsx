import { useRef, useEffect } from 'react';
import '../Styles/Canvas.css';

function Canvas({ width, height, objects }) {
    const canvasRef = useRef(null);
    const objectsRef = useRef([]);

    const lastUpdateRef = useRef(Date.now());
    const prevPosRef = useRef({ x: 0, y: 0 });
    const nextPosRef = useRef({ x: 0, y: 0 });
    const secondObject = useRef({ x: 0, y: 0 });


    const scoreObject = useRef({ taggerScore: 0, runnerScore: 0 });
    const timer = useRef(0);

    //I have much more comments in this section cuz the canvas code is rather complex

    //Note, I can't use objects states directly in canvas, it just doesn't work, so I create these references to use the data
    useEffect(() => {
        objectsRef.current = objects;

        if (objects.runner && objects.tagger && objects.scores) {
            prevPosRef.current.x = nextPosRef.current.x;
            prevPosRef.current.y = nextPosRef.current.y;
            nextPosRef.current.x = objects.runner.x;
            nextPosRef.current.y = objects.runner.y;
            secondObject.current.x = objects.tagger.x;
            secondObject.current.y = objects.tagger.y;
            lastUpdateRef.current = Date.now();

            scoreObject.current.taggerScore = objects.scores.taggerScore;
            scoreObject.current.runnerScore = objects.scores.runnerScore;

            timer.current = objects.timer.time;
        }

    }, [objects]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let animationId;

        function loop() {
            context.clearRect(0, 0, width, height);

            const g = context.createLinearGradient(0, 0, 0, height);
            g.addColorStop(0, '#03060a');
            g.addColorStop(1, '#071018');
            context.fillStyle = g;
            context.fillRect(0, 0, width, height);

            context.save();
            context.globalAlpha = 0.06;
            context.strokeStyle = '#ffffff';
            context.lineWidth = 1;
            const step = Math.max(24, Math.round(Math.min(width, height) / 24));
            for (let x = 0.5; x < width; x += step) {
                context.beginPath();
                context.moveTo(x, 0);
                context.lineTo(x, height);
                context.stroke();
            }
            for (let y = 0.5; y < height; y += step) {
                context.beginPath();
                context.moveTo(0, y);
                context.lineTo(width, y);
                context.stroke();
            }
            context.restore();

            const t = Math.min((Date.now() - lastUpdateRef.current) / 33, 1);
            const interpX = prevPosRef.current.x + (nextPosRef.current.x - prevPosRef.current.x) * t;
            const interpY = prevPosRef.current.y + (nextPosRef.current.y - prevPosRef.current.y) * t;

            //Drawing the interpolated Runner, must switch color
            context.save();
            context.shadowColor = '#4da6ff';
            context.shadowBlur = 18;
            context.fillStyle = '#4da6ff';

            context.beginPath();
            context.arc(interpX + 15, interpY + 15, 15, 0, Math.PI * 2);
            context.fill();
            context.restore();
            //small inner circle
            context.fillStyle = '#fff';
            context.beginPath();
            context.arc(interpX + 15, interpY + 15, 5, 0, Math.PI * 2);
            context.fill();

            // Label for Runner
            context.save();
            context.font = '12px sans-serif';
            context.textAlign = 'center';
            context.textBaseline = 'bottom';
            // small semi-transparent background for legibility
            const runnerLabel = 'Runner';
            const rx = interpX + 15;
            const ry = interpY - 4;
            const padding = 6;
            const metrics = context.measureText(runnerLabel);
            const labelW = metrics.width + padding;
            const labelH = 16;
            context.fillStyle = 'rgba(0,0,0,0.5)';
            context.fillRect(rx - labelW / 2, ry - labelH, labelW, labelH);
            context.fillStyle = '#d6edff';
            context.fillText(runnerLabel, rx, ry - 4);
            context.fillText('Runner: '+ scoreObject.current.runnerScore, 350, 30)
            context.restore();
        

            //Draw Tagger, raw position, observe if I need interp
            context.save();
            context.shadowColor = '#ff4d4f';
            context.shadowBlur = 18;
            context.fillStyle = '#ff4d4f';
            context.beginPath();
            context.arc(secondObject.current.x + 15, secondObject.current.y + 15, 15, 0, Math.PI * 2);
            context.fill();
            context.restore();
            //Small Chaser circle
            context.fillStyle = '#fff';
            context.beginPath();
            context.arc(secondObject.current.x + 15, secondObject.current.y + 15, 5, 0, Math.PI * 2);
            context.fill();

            // Label for Tagger
            context.save();
            context.font = '12px sans-serif';
            context.textAlign = 'center';
            context.textBaseline = 'bottom';
            const chaserLabel = 'Tagger';
            const cx = secondObject.current.x + 15;
            const cy = secondObject.current.y - 4;
            const paddingC = 6;
            const metricsC = context.measureText(chaserLabel);
            const labelWC = metricsC.width + paddingC;
            const labelHC = 16;
            context.fillStyle = 'rgba(0,0,0,0.5)';
            context.fillRect(cx - labelWC / 2, cy - labelHC, labelWC, labelHC);
            context.fillStyle = '#ffb3b6';
            context.fillText(chaserLabel, cx, cy - 4);
            context.fillText('Tagger: '+ scoreObject.current.taggerScore, 450, 30);
            context.restore();


            //timer
            context.fillStyle = '#FFFFFF';
            context.font = '20px sans-serif';
            context.fillText(timer.current, 395, 30);
            animationId = requestAnimationFrame(loop);
        }

        animationId = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(animationId);
    }, [width, height]);

    return <canvas className="canvas" ref={canvasRef} width={width} height={height} />;
}
export default Canvas;