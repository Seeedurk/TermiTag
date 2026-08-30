import { useState } from 'react';
import '../Styles/SettingsModal.css';

const runnerDescriptions = {
    1: 'Untrained Model, literal newborn baby playing tag.',
    2: 'Model trained on 2500 episodes, learned basic running and environmental awareness.',
    3: 'Model trained on 5000 episodes, learned evasive manuevers and wall usage.',
    4: 'Custom: This is what you select if you decide to train your own model! Follow the github/readMe instructions for more.'
};

const taggerDescriptions = {
    1: 'Accelerates torwards runner rudimentarily. The most basic possible version.',
    2: 'Can plan ahead in time, using functions to find the best moves 30 steps in the future',
    3: 'Not only can plan ahead, but also predicts runners trajectory and cut them off. Absolute terminator.',
    4: 'Play by guiding the Tagger with your Mouse!. Lets see if you can beat some lines of code.'
};

function LevelSelector({ title, name, value, onSelect, accent, descriptions }) {
    const levels = [1, 2, 3, 4];
    const selectedLevel = Number(value) || 1;

    return (
        <div className="level-selector">
            <div className="level-header">
                <span>{title}</span>
            </div>
            <div className="level-buttons" role="group" aria-label={title}>
                {levels.map((level) => {
                    const isSelected = selectedLevel === level;
                    const intensity = level / levels.length;
                    const hue = accent === 'runner' ? 197 : 0;
                    const saturation = accent === 'runner' ? 71 : 76;
                    const lightness = isSelected ? 45 + intensity * 10 : 88;

                    return (
                        <button
                            key={level}
                            type="button"
                            className={isSelected ? 'level-button selected' : 'level-button'}
                            onClick={() => onSelect(name, level)}
                            style={isSelected ? {
                                background: `hsl(${hue} ${saturation}% ${lightness}%)`,
                                borderColor: accent === 'runner' ? '#0f6176' : '#af2d2d',
                                color: '#ffffff',
                                boxShadow: `0 0 0 1px ${accent === 'runner' ? '#0f6176' : '#af2d2d'}, 0 8px 18px rgba(0,0,0,0.12)`
                            } : {
                                background: 'transparent',
                                borderColor: accent === 'runner' ? '#8ec2d1' : '#d9a0a0',
                                color: accent === 'runner' ? '#0f6176' : '#7c2020'
                            }}
                        >
                            {level}
                        </button>
                    );
                })}
            </div>
            <p className="level-description">{descriptions[selectedLevel] || descriptions[1]}</p>
        </div>
    );
}

function SettingsModal({ initialSettings, onSubmit, onClose }) {
    const [settings, setSettings] = useState(() => Object.fromEntries(
        Object.entries(initialSettings).map(([key, value]) => [
            key,
            typeof value === 'number' ? String(value) : value
        ])
    ));

    const handleChange = (event) => {
        const { name, value } = event.target;
        setSettings((currentSettings) => ({
            ...currentSettings,
            [name]: value
        }));
    };

    const handleLevelSelect = (name, level) => {
        setSettings((currentSettings) => ({
            ...currentSettings,
            [name]: String(level)
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        const normalizedSettings = Object.fromEntries(
            Object.entries(settings).map(([key, value]) => {
                if (typeof value === 'string' && value.trim() !== '') {
                    const parsed = Number(value);
                    return [key, Number.isNaN(parsed) ? value : parsed];
                }
                return [key, value];
            })
        );

        onSubmit(normalizedSettings);
        onClose();
    };

    const wallCountLocked = Boolean(settings.randomizeNumberOfWalls);
    const playerPositionsLocked = Boolean(settings.randomizePlayerPositions);

    return (
        <div className="settings-backdrop" role="presentation" onMouseDown={onClose}>
            <div className="settings-modal" role="dialog" aria-modal="true" aria-labelledby="settings-title" onMouseDown={(event) => event.stopPropagation()}>
                <div className="settings-header">
                    <h2 id="settings-title">Game settings</h2>
                    <button type="button" className="settings-close" onClick={onClose} aria-label="Close settings">&times;</button>
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="level-stack">
                        <LevelSelector
                            title="Runner level"
                            name="desiredRunnerLevel"
                            value={settings.desiredRunnerLevel}
                            onSelect={handleLevelSelect}
                            accent="runner"
                            descriptions={runnerDescriptions}
                        />
                        <LevelSelector
                            title="Tagger level"
                            name="desiredTaggerLevel"
                            value={settings.desiredTaggerLevel}
                            onSelect={handleLevelSelect}
                            accent="tagger"
                            descriptions={taggerDescriptions}
                        />
                    </div>

                    <div className="settings-fields">
                        {Object.entries(settings).filter(([, value]) => typeof value === 'string' || typeof value === 'number').map(([name, value]) => {
                            if (name === 'desiredRunnerLevel' || name === 'desiredTaggerLevel') {
                                return null;
                            }

                            const isLocked =
                                (name === 'numberOfWalls' && wallCountLocked) ||
                                (['runnerStartX', 'runnerStartY'].includes(name) && playerPositionsLocked) ||
                                (['taggerStartX', 'taggerStartY'].includes(name) && playerPositionsLocked);

                            return (
                                <label key={name}>
                                    {name === 'numberOfWalls'
                                        ? 'Number of walls'
                                        : name.replace(/([A-Z])/g, ' $1').trim()}
                                    <input
                                        name={name}
                                        type="number"
                                        value={value}
                                        onChange={handleChange}
                                        min="0"
                                        required
                                        disabled={isLocked}
                                    />
                                </label>
                            );
                        })}
                    </div>
                    <label className="settings-checkbox">
                        <input
                            name="randomizeNumberOfWalls"
                            type="checkbox"
                            checked={settings.randomizeNumberOfWalls}
                            onChange={(event) => setSettings((currentSettings) => ({
                                ...currentSettings,
                                randomizeNumberOfWalls: event.target.checked
                            }))}
                        />
                        Random wall count (0-5)
                    </label>
                    {wallCountLocked ? (
                        <p className="settings-note">Locked: wall count is randomized, so the fixed wall count input is unavailable.</p>
                    ) : null}
                    <label className="settings-checkbox">
                        <input
                            name="randomizePlayerPositions"
                            type="checkbox"
                            checked={settings.randomizePlayerPositions}
                            onChange={(event) => setSettings((currentSettings) => ({
                                ...currentSettings,
                                randomizePlayerPositions: event.target.checked
                            }))}
                        />
                        Random player positions
                    </label>
                    {playerPositionsLocked ? (
                        <p className="settings-note">Locked: player spawn positions are randomized, so fixed runner and tagger positions are unavailable.</p>
                    ) : null}
                    <button type="submit" className="settings-submit">Submit</button>
                </form>
            </div>
        </div>
    );
}

export default SettingsModal;



