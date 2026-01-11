import { useRef, useEffect } from 'react';
import '../Styles/Canvas.css';

function Canvas({width, height, objects}) {
    const canvasRef = useRef(null);
    const objectsRef = useRef([]);
    const lastUpdateRef = useRef(Date.now());

    const prevPosRef = useRef({ x: 0, y: 0 });
    const nextPosRef = useRef({ x: 0, y: 0 });

    useEffect(() => {
        objectsRef.current = objects;
        if (objectsRef.current.length > 0) {

            prevPosRef.current.x = nextPosRef.current.x;
            prevPosRef.current.y = nextPosRef.current.y;

            nextPosRef.current.x = objects[0].x;
            nextPosRef.current.y = objects[0].y;

            lastUpdateRef.current = Date.now();
        }
    }, [objects]);

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let animationId;

        function loop() {
            context.fillStyle = 'red';
            context.clearRect(0, 0, width, height);


            const t = Math.min((Date.now() - lastUpdateRef.current) / 33, 1); 
            const interpX = prevPosRef.current.x + (nextPosRef.current.x - prevPosRef.current.x) * t;
            const interpY = prevPosRef.current.y + (nextPosRef.current.y - prevPosRef.current.y) * t;

            context.fillRect(interpX, interpY, 20, 30);
            animationId = requestAnimationFrame(loop);
        }


        animationId = requestAnimationFrame(loop);


        return () => cancelAnimationFrame(animationId);
    }, [width, height]);

   

    return <canvas className="canvas" ref={canvasRef} width={width} height={height} />;

}
export default Canvas;