import react from 'react';
import '../Styles/Help.css';

function Help() {
    const [toggled, setToggled] = react.useState("open");

    return (
        <div className={`Help ${toggled ? "open": "closed"} `} > A brief treatise of instruction</div>
    );
}

export default Help;