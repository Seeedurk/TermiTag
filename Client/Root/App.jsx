import { useState, useEffect, useRef } from 'react'
import '../Styles/App.css'
import Canvas from '../Components/Canvas';
import Navbar from '../Components/Navbar';
import Menu from '../Components/Menu';


function App() {
    /* cd C:\Users\sedri\Projects\TermiTank */



    return (
    <>
        <Navbar />
            <Menu /> 

        <div className="main-div">

                <h1 className="title">TermiTank</h1>
                <div className="game-window">
                    <Canvas width={1000} height={500} />
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
