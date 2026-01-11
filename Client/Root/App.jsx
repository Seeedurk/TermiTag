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
            setObjects([data]);
        });


       
        return () => {
            socket.off("init_response");
            socket.off("position_update");
        }
        
    }, [objects])

    return (
    <>
        <Navbar />
            <Menu /> 

        <div className="main-div">

                <h1 className="title">TermiTank</h1>
                <div className="game-window">
                    <Canvas width={1000} height={500} objects={objects} />
                </div>


                <h1>You Are Doomed</h1>
                <p className="read-the-docs">
                    How many models can you destroy?
                </p>

        </div>
       
        

    </>
  )
}

export default App
