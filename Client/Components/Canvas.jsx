import { useRef, useEffect } from 'react';
import '../Styles/Canvas.css';

function Canvas({width, height }) {
    const canvasRef = useRef(null);
    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let animationId;

        function loop() {
            context.clearRect(0, 0, width, height);
            context.fillStyle = 'red';
            context.fillRect(0, 50, 20, 30);
            context.save();
            context.translate(1, 1);
            animationId = requestAnimationFrame(loop);
        }

        // start the loop
        animationId = requestAnimationFrame(loop);

        // cleanup when component unmounts or dependencies change
        return () => cancelAnimationFrame(animationId);
    }, [width, height]);

   

    return <canvas className="canvas" ref={canvasRef} width={width} height={height} />;

}
export default Canvas;