import { useState, useEffect } from 'react';
import '../Styles/Menu.css';

function Menu() {
    const [open, setOpen] = useState(true);

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

    return (
        <div className={`Menu ${open ? 'open' : 'closed'}`} aria-expanded={open}>
            <button className="menu-toggle" onClick={() => setOpen((v) => !v)} aria-label="Toggle menu">
                {open ? 'Close' : 'Menu'}
            </button>

            <div className="menu-body">
                <h2>Menu</h2>
                <p>This will be where both statisics and game customization will go.</p>
                <button>Run 2 AI Tagger simulation</button>
                <button>Run 1 AI Tagger vs 1 Human simulation</button>
                <button>Statistical analysis</button>
            </div>
        </div>
    );
}

export default Menu;