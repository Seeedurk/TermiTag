import { useState, useEffect, useRef } from 'react'
import '../Styles/App.css'
import Canvas from '../Components/Canvas';
import Navbar from '../Components/Navbar';
import Menu from '../Components/Menu';
import socket from '../Components/Socket';

function App() {

    const effectRan = useRef(false);


    const [objects, setObjects] = useState([]);
    /* cd C:\Users\sedri\Projects\TermiTank */
    useEffect(() => {

        socket.on("connect", () => {
            console.log("Connected to server with ID:", socket.id);
            socket.emit("init", "Hello");
        }); 

            

        socket.on("init_response", (data) => { console.log(data) });
        socket.on("position_update", (data) => {
            setObjects(data);
        });


       
        return () => {
            socket.off("init_response");
            socket.off("position_update");
        }
        
    }, [objects])

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

                    <Menu />
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
