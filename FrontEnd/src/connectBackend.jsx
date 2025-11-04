import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css"
export default function Connecting({setErr, error, userInp, setInp}){
    // const api = import.meta.env.VITE_API_URL;
    const navigate = useNavigate();
    // const [currentInfo, setInfo] = useState("")
    // const [userInp, setInp] = useState("")

    // const navigatingError=()=>{
    //     navigate('/error')
    // }  
    
    const navigatingNext=()=>{
        navigate('/charDesignEvery')
    }  
    
    const newAiCall = async (e)=>{
        try{
        e.preventDefault();
        const addData = await fetch(`http://127.0.0.1:8000/start_llm_server/`, {
            method: "POST",
            headers:{"Content-Type": "application/json"},
            body: JSON.stringify({
                "user_name": `${userInp}`,
                "llm_model_name": "string",
                "mode": "new_console",
                "chat_template":"chatml"
            })
        }
        )
        let newData = await addData.json();
        //since its always true, i just gonna add this for decoration .-.
        if(newData.is_LLM_server_started){
            // setInfo("Success")
            const das = setInterval(()=>{navigatingNext(), clearInterval(das)}, 5000)
        }else{
            setErr(e.llm_server_info);
        }
        }catch(e){
            setErr(e.llm_server_info)
            console.log(e)
            // navigatingError()
        }
    }
    return(
        <div className="backGrandScrollOverf">
            <div className="allignForm">
                <form onSubmit={newAiCall}>
                    <pre>Enter your name, AI hope to know more about
                        your private information 🥰🥰🥰
                    </pre>
                    <input type="text" value={userInp} onChange={e=>setInp(e.target.value)}></input>
                    <button type="submit">Connect to AI now</button>
                    {(error!="")?(<p>{error}</p>):("")}
                </form>
            </div>
        </div>
    )
}