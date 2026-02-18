import { useRef, useEffect } from 'react';
import '../Styles/Canvas.css';

function Canvas({ width, height, objects }) {
    const canvasRef = useRef(null);
    const objectsRef = useRef([]);
    const lastUpdateRef = useRef(Date.now());
    const prevPosRef = useRef({ x: 0, y: 0 });
    const nextPosRef = useRef({ x: 0, y: 0 });
    const tempPosRef = useRef({ x: 0, y: 0 });

    useEffect(() => {
        objectsRef.current = objects;
        if (objectsRef.current.length > 0) {
            prevPosRef.current.x = nextPosRef.current.x;
            prevPosRef.current.y = nextPosRef.current.y;
            nextPosRef.current.x = objects[0].x;
            nextPosRef.current.y = objects[0].y;
            tempPosRef.current.x = objects[1].x;
            tempPosRef.current.y = objects[1].y;
            lastUpdateRef.current = Date.now();
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

            context.save();
            context.shadowColor = '#ff4d4f';
            context.shadowBlur = 18;
            context.fillStyle = '#ff4d4f';
            context.beginPath();
            context.arc(interpX + 15, interpY + 15, 15, 0, Math.PI * 2);
            context.fill();
            context.restore();

            context.fillStyle = '#fff';
            context.beginPath();
            context.arc(interpX + 15, interpY + 15, 5, 0, Math.PI * 2);
            context.fill();

            context.save();
            context.shadowColor = '#4da6ff';
            context.shadowBlur = 18;
            context.fillStyle = '#4da6ff';
            context.beginPath();
            context.arc(tempPosRef.current.x + 15, tempPosRef.current.y + 15, 15, 0, Math.PI * 2);
            context.fill();
            context.restore();

            context.fillStyle = '#fff';
            context.beginPath();
            context.arc(tempPosRef.current.x + 15, tempPosRef.current.y + 15, 5, 0, Math.PI * 2);
            context.fill();

            animationId = requestAnimationFrame(loop);
        }

        animationId = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(animationId);
    }, [width, height]);

    return <canvas className="canvas" ref={canvasRef} width={width} height={height} />;
}
export default Canvas;