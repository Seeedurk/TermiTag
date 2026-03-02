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
                <h1>Simulation only on Mobile, Use Laptop to play against AI</h1>
                <p className="read-the-docs">
                        This project is meant to be a showcase of AI taggers playing against each other in a simple 2D environment.
                        Using WebSockets and Neural Networks, their fight can be rendered here in real-time.
                        Use the Menu on the right to select the parameters of the game and enjoy!
                </p>

                    


        </div>
       
        

    </>
  )
}

export default App
