import { useState } from "react";
import { useNavigate, useNavigate } from "react-router-dom";
export default function Connecting({setErr}){
    const navigate = useNavigate();
    const [currentInfo, setInfo] = useState("")

    const navigatingError=()=>{
        navigate('/error')
    }  
    
    const navigatingNext=()=>{
        navigate('/charDesign')
    }  
    
    const newAiCall = async ()=>{
        try{
        const addData = await fetch(`${api}/chat_with_character/`, {
            method: "POST",
            headers:{"Content-Type": "application/json"},
            body: JSON.stringify({
                "mode": "???",
                "chat_template":"???"
            })
        }
        )
        let newData = addData.json();
        //since its always true, i just gonna add this for decoration .-.
        if(newData.is_LLM_server_started){
            setInfo(newData.llm_server_info)
            const das = setInterval(()=>{navigatingNext(), clearInterval(das)}, 5000)
        }else{
            setErr(e.llm_server_info)
        }
        }catch(e){
            setErr(e.llm_server_info)
            navigatingError()
        }
    }
    return(
        <div>
            {(currentInfo=="")?(
                <button onSubmit={newAiCall} >Connect to AI now</button>
            ):(<pre>{currentInfo}</pre>)
            }
        </div>
    )
}