import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import SetMbti from "./setMbti";

export default function InformationNew(){
    const api = import.meta.env.VITE_API_URL;
    const [check1, checkLock1] = useState([])
    const [check2, checkLock2] = useState([])
    //all availble char
    const [characters, setCharacters] = useState([])
    //pick the char
    const [chosenChar, setChoosenChar] = useState("")
    const [chosenFile, setChoosenFile] = useState("")
    //eror handler
    const [theError, setErr] = useState("")
    const navigating = useNavigate();

    useEffect(()=>{
        const callSync=async ()=>{
            try{
                const listOfChar = await fetch(`${api}show_saved_characters/`)
                if (!listOfChar.ok) {alert("Failed to fetch characters"); return};
                let getList = await listOfChar.json();
                setCharacters(getList.Characters)
                setErr(e.message||getList.error_detail||"No character found")
            }catch(e){
                setErr(e.message||"No character found")
            }
        }
        callSync()
    },[])

    const putChar = async (e)=>{
        try{
            e.preventDefault();
            const changeCharac = await fetch(`${api}load_character/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"user_name": chosenChar,"character_file_name": chosenFile})
            })
            let res
            if(changeCharac.ok){
                res = await changeCharac.json()
                if(res.is_normal&&res.is_char_exists)
                    checkLock2(true)
            }
            if(!changeCharac.ok)setErr(res.error_detail||"Failed to load")
        }catch(e){
            setErr(e.message||"Error occured in making character")
        }
    }

    //navigate next step for generating character
    useEffect(()=>{
        if(check1&&check2)
            navigating("/chatNow")
    }, [check2, check1])

    return(
        <div>
            {(theError=="")?(""):(<p>theError</p>)}
            <form onSubmit={putChar}>
                <label>
                    What's your name?
                    <input value={chosenChar} onChange={(e)=>setChoosenChar(e.target.value)} type="text"></input>
                </label>
                <select value={chosenFile} onChange={(e)=>setChoosenFile(e.target.value)}>
                    {characters.map((e,i)=>(
                        //this part is confusing, no doc yet
                        <option value={e.characterName} key={i}>{e.characterName}</option>
                    ))}
                </select>
                <button type="submit">Submit here</button>
            </form>
            <SetMbti checkLock1={checkLock1} setErr={setErr} chosenChar={chosenChar} />
        </div>
    )

}