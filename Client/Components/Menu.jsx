import { useState, useEffect } from 'react';
import '../Styles/Menu.css';
import DistanceGraph from './DistanceGraph';
import RewardGraph from './RewardGraph';
import socket from '../Components/Socket';

function Menu( { rewardGraphData, distanceGraphData } ) {
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
                <h3>Statistics - Distance & Reward</h3>
                <DistanceGraph key="distance-graph-1" data={distanceGraphData} />

                <RewardGraph key="reward-graph-2" data={rewardGraphData} />
                </div>
            </div>
        </div>
    );
}

export default Menu;