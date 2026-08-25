import { useState, useEffect, useRef } from 'react'
import '../Styles/App.css'
import Canvas from '../Components/Canvas';
import Navbar from '../Components/Navbar';
import Menu from '../Components/Menu';
import socket from '../Components/Socket';

function App() {

    const effectRan = useRef(false);


    const [objects, setObjects] = useState([]);
    const [distanceData, setDistanceData] = useState([])
    const [rewardData, setRewardData] = useState([])

    const lastGraphUpdate = useRef(0);


    useEffect(() => {
        const handleConnect = () => {
            console.log("Connected to server with ID:", socket.id);
            socket.emit("init", "Hello");
        };

        const handleInitResponse = (data) => {
            console.log(data);
        };

        const handlePositionUpdate = (data) => {
            setObjects(data);

            const now = performance.now();

            if (now - lastGraphUpdate.current < 100) {
                return;
            }

            lastGraphUpdate.current = now;

            setDistanceData((currentData) => [
                ...currentData.slice(-24),
                {
                    step: currentData.length
                        ? currentData[currentData.length - 1].step + 1
                        : 0,
                    distance: Number(data.distance.toFixed(2))
                }
            ]);

            setRewardData((currentData) => [
                ...currentData.slice(-24),
                {
                    step: currentData.length
                        ? currentData[currentData.length - 1].step + 1
                        : 0,
                    reward: Number(data.reward.toFixed(2))
                }
            ]);
        };

        socket.on("connect", handleConnect);
        socket.on("init_response", handleInitResponse);
        socket.on("position_update", handlePositionUpdate);

        return () => {
            socket.off("connect", handleConnect);
            socket.off("init_response", handleInitResponse);
            socket.off("position_update", handlePositionUpdate);
        };
    }, []);

    /*I can move graph if I want other format*/
    return (
    <>
        <Navbar />


        <div className="main-div">

                
                <h1 className="title">TermiTag</h1>
                <div className="middle-div">
                    <div className="game-window">
                        <Canvas width={800} height={600} objects={objects} />
                    </div>

                    <Menu rewardGraphData={rewardData} distanceGraphData={distanceData}/>
                </div>




                <h1>Neural Network Tag</h1>
                <h2>This is an AI, and no it's not chatGPT</h2>
                <p className="read-the-docs">
                        What you're currently seeing is a Neural Network play against a Neural Network.
                        The specific model used to train these agents is a double DQN utilizing mind numbing but relatively simple AI theory.
                        If you take a look at the code you can see the training loop, architecture, and tools used to create these AI's.
                        As well as that you can use the functionalities of the frontend to see stats like loss, reward, and more. Have fun!
                </p>

                    


        </div>
       
        

    </>
  )
}

export default App
