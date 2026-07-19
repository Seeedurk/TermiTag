import { useState, useEffect } from 'react';
import '../Styles/Menu.css';
import LossGraph from '../Components/LossGraph';
import socket from '../Components/Socket';

function Menu() {
    const [open, setOpen] = useState(true);
    const [paused, setPause] = useState(false);

    useEffect(() => {
        const mq = window.matchMedia('(max-width: 700px)');
        const onChange = (e) => setOpen(!e.matches);
        setOpen(!mq.matches);
        if (mq.addEventListener) mq.addEventListener('change', onChange);
        else mq.addListener(onChange);
        return () => {
            if (mq.removeEventListener) mq.removeEventListener('change', onChange);
            else mq.removeListener(onChange);
        };
    }, []);

    const handlePause = () => {
        socket.emit('pause', !paused)
        setPause(!paused)
    }

    const handleReset = () => {
        socket.emit('reset')
    }

    return (
        <div className={`Menu ${open ? 'open' : 'closed'}`} aria-expanded={open}>
            <button className="menu-toggle" onClick={() => setOpen((v) => !v)} aria-label="Toggle menu">
                {open ? 'Close' : 'Menu'}
            </button>

            <div className="menu-body">
                <h2>Menu</h2>
                <p>This will be where both statisics and game customization will go.</p>
                <button onClick={handlePause} style={{
                    backgroundColor: "red",
                    color: "white",
                    border: "none",
                    padding: "8px 16px",
                    borderRadius: "6px",
                    boxShadow: "0 0 12px rgba(255, 0, 0, 0.6)",
                    width: "30%"

                 }}>{paused ? "Resume" : "Pause"}</button>
                <button onClick = {handleReset} style={{
                    backgroundColor: "black",
                    color: "white",
                    border: "none",
                    padding: "8px 16px",
                    borderRadius: "6px",
                    boxShadow: "0 0 12px rgba(0, 0, 0, 0.6)",
                    width: "30%"
                }}>Restart</button>
                <button style={{width:"40%", height: "5%"} }>Settings</button>

                <div className="stat-div" >
                <h3>Statistics - add all to bottom</h3>
                <LossGraph key="loss-graph-1" data={[
                    { step: 1, loss: 0.9 },
                    { step: 2, loss: 0.7 },
                    { step: 3, loss: 0.5 },
                    { step: 4, loss: 0.4 },
                    { step: 5, loss: 0.35 },
                    { step: 6, loss: 0.3 },
                    { step: 7, loss: 0.28 },
                    { step: 8, loss: 0.25 }
                ]} />

                <LossGraph key="loss-graph-2" data={[
                    { step: 1, loss: 0.9 },
                    { step: 2, loss: 0.7 },
                    { step: 3, loss: 0.5 },
                    { step: 4, loss: 0.4 },
                    { step: 5, loss: 0.35 },
                    { step: 6, loss: 0.3 },
                    { step: 7, loss: 0.28 },
                    { step: 8, loss: 0.25 }
                ]} />
                </div>
            </div>
        </div>
    );
}

export default Menu;