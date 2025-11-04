import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function FormChoose({userInp}){
    // const api = import.meta.env.VITE_API_URL;
    const [savedFile, setCharFile] = useState();
    const [error, setError] = useState("");
    const [choosenChar, setChar] = useState();
    const [abstract, setAbs] = useState("");
    const navigating = useNavigate();

    const [loading, setLoad] = useState(false)

    useEffect(()=>{
        const callSync=async ()=>{
            try{
                const listOfChar = await fetch(`http://127.0.0.1:8000/show_saved_characters/`)
                if (!listOfChar.ok) {
                    setError(e.message||getList.error_detail||"No character found");
                    alert(error); 
                    return};
                let getList = await listOfChar.json();
                setCharFile(getList)
            }catch(e){
                setError(e.message||"No character found")
            }
        }
        callSync()
    },[])
    
    const sendOver = async (e)=>{
        try{
            setLoad(true);
            e.preventDefault();
            // let changeChar = choosenChar;
            // changeChar["user_name"]=userInp;
            // changeChar["is_this_char_target"]=true;
            const res = await fetch(`http://127.0.0.1:8000/load_character/`, {
                method: "PUT",
                headers:{
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({"character_file_name":abstract})
            })
            if(!res.ok){alert("Something is wrong"); setLoad(false)}

            const catching = await res.json();

            if(catching.is_normal){
                if(catching.is_char_exists)
                    navigating("/chatNow")
            }            
        }catch(e){

        }
    }

    return(
        <div>
            {(loading)?(<h1>Loading</h1>):(
                <div>
                    <div>
                        <input type="text" onChange={e=>setAbs(e.target.value)} value={abstract} placeholder="Type somethign here"></input>
                        <button onClick={e=>sendOver(e)}>Search</button>
                    </div>
                    <p>{error}</p>
                    {
                    //true then filter
                    //&& data['Vote date'] != typingDate not working properly and some dates repeating
                    abstract.length!=0 && savedFile["Characters"].filter(item => item["file_name"].startsWith(abstract) && item['file_name'] != abstract)
                    .map((data, i)=>(
                        ""!=data["file_name"]?(
                            <div className="findItems" key={i} onClick={()=>{setChar(data), setError(""), setAbs(data["file_name"])}}>
                                {data["file_name"]}
                            </div>
                        ):("")
                    ))
                    }
                </div>
            )
            }
        </div>
    )
}