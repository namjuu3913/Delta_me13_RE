import { useState, useEffect } from "react";
import "../App.css"

export default function InputPButton({loading, setLoad, setUserMessages, disable, setDis}){
    const [currentMessage, setMessage] = useState("");
    useEffect(()=>{
        if(currentMessage.length==0)
            setDis(true)
        else if(!loading && currentMessage.length!=0)
            setDis(false)
    }, [currentMessage]
    )
    const changeCurrent = (e)=>{
        e.preventDefault()
        setDis(true)
        setLoad(true)
        let currentUserPOst = {messages: currentMessage, sender: "User"}
        setUserMessages(prev => [...prev, currentUserPOst])
        setMessage("")
        // setUserMessages(currentMessage);
    }
    return(
        <div className="interactionArea">
            {console.log(currentMessage)}
            <form onSubmit={changeCurrent}>
                <textarea rows={3} cols={100} value={currentMessage} placeholder="Type something here" onChange={e=>setMessage(e.target.value)}></textarea>
                {(disable)?(<div className="buttonImitation">Hold on</div>):(<button type="submit" className="circlwithPointer">Send</button>)}
            </form>
            <p>Press the Send button to send</p>
        </div>
    )
}