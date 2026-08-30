import { useState, useEffect } from 'react';
import '../Styles/Menu.css';
import DistanceGraph from './DistanceGraph';
import RewardGraph from './RewardGraph';
import SettingsModal from './SettingsModal';
import socket from '../Components/Socket';

const defaultSettings = {
    timeLimit: 10,
    desiredRunnerLevel: 1,
    desiredTaggerLevel: 1,
    runnerStartX: 100,
    runnerStartY: 300,
    taggerStartX: 700,
    taggerStartY: 300,
    numberOfWalls: 2,
    randomizeNumberOfWalls: true,
    randomizePlayerPositions: true,
};

function Menu( { rewardGraphData, distanceGraphData } ) {
    const [open, setOpen] = useState(true);
    const [paused, setPause] = useState(false);
    const [settings, setSettings] = useState(defaultSettings);
    const [settingsOpen, setSettingsOpen] = useState(false);
    const [view, setView] = useState('stats');

    useEffect(() => {
        const mq = window.matchMedia('(max-width: 700px)');
        const onChange = (e) => setOpen(!e.matches);
        setOpen(!mq.matches);

        if (mq.addEventListener) mq.addEventListener('change', onChange);
        else mq.addListener(onChange);

        const handleSettingsResponse = (payload) => {
            setSettings({ ...defaultSettings, ...payload });
        };

        socket.on('settings_response', handleSettingsResponse);

        return () => {
            if (mq.removeEventListener) mq.removeEventListener('change', onChange);
            else mq.removeListener(onChange);
            socket.off('settings_response', handleSettingsResponse);
        };
    }, []);

    const handlePause = () => {
        socket.emit('pause', !paused)
        setPause(!paused)
    }

    const handleReset = () => {
        socket.emit('reset')
    }

    const handleSettingsSubmit = (nextSettings) => {
        const payload = { ...defaultSettings, ...nextSettings };
        setSettings(payload);
        socket.emit('settings', payload);
    };

    return (
        <div className={`Menu ${open ? 'open' : 'closed'}`} aria-expanded={open}>
            <button className="menu-toggle" onClick={() => setOpen((v) => !v)} aria-label="Toggle menu">
                {open ? 'Close' : 'Menu'}
            </button>

            <div className="menu-body">
                <h2>Menu</h2>
                <p>This will be where both statisics and game customization will go.</p>
                <div className="action-row">
                    <button onClick={handlePause} style={{
                        backgroundColor: "red",
                        color: "white",
                        border: "none",
                        padding: "8px 16px",
                        borderRadius: "6px",
                        boxShadow: "0 0 12px rgba(255, 0, 0, 0.6)",
                        flex: 1,
                        margin: 0
                     }}>{paused ? "Resume" : "Pause"}</button>
                    <button onClick = {handleReset} style={{
                        backgroundColor: "black",
                        color: "white",
                        border: "none",
                        padding: "8px 16px",
                        borderRadius: "6px",
                        boxShadow: "0 0 12px rgba(0, 0, 0, 0.6)",
                        flex: 1,
                        margin: 0
                    }}>Restart</button>
                    <button onClick={() => setSettingsOpen(true)} style={{
                        backgroundColor: "#0f6176",
                        color: "white",
                        border: "none",
                        padding: "8px 12px",
                        borderRadius: "6px",
                        boxShadow: "0 0 12px rgba(15, 97, 118, 0.6)",
                        flex: 1,
                        margin: 0,
                        fontSize: "0.9rem"
                    }}>Settings</button>
                </div>

                <div className="view-switch" role="group" aria-label="Menu view">
                    <button className={view === 'stats' ? 'active' : ''} onClick={() => setView('stats')}>Stats</button>
                    <button className={view === 'algorithm' ? 'active' : ''} onClick={() => setView('algorithm')}>Algorithm</button>
                </div>

                {settingsOpen ? (
                    <SettingsModal
                        initialSettings={settings}
                        onSubmit={handleSettingsSubmit}
                        onClose={() => setSettingsOpen(false)}
                    />
                ) : null}

                {view === 'algorithm' ? (
                    <div className="algorithm-panel">
                        <p>
                            This game uses a double DQN-driven runner and a pursuit model for the tagger.
                            The runner learns from state, reward shaping, and wall/edge danger, while the tagger
                            evaluates candidate accelerations against the runner's current position.
                        </p>
                    </div>
                ) : (
                    <div className="stat-div" >
                        <DistanceGraph key="distance-graph-1" data={distanceGraphData} />

                        <RewardGraph key="reward-graph-2" data={rewardGraphData} />
                    </div>
                )}
            </div>
        </div>
    );
}

export default Menu;