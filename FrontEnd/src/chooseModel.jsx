import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function InformationNew(){
    const api = import.meta.env.VITE_API_URL;
    //all availble char
    const [characters, setCharacters] = useState([])
    //pick the char
    const [chosenChar, setChoosenChar] = useState("")
    const [chosenFile, setChoosenFile] = useState("")
    //set MBTI
    // const [mbti, setmbti] = useState("")
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
            let res = await changeCharac.json()
            if(changeCharac.ok)alert("Character finish")
            if(!changeCharac.ok)setErr(res.error_detail||"Failed to load")
        }catch(e){
            setErr(e.message||"Error occured in making character")
        }
    }

    // const setMBTI = async ()=>{
    //     try{
    //         const changeCharac = await fetch(`${api}change_character_personality/`, {
    //             method: PATCH,
    //             headers: {
    //                 "Content-Type": "application/json"
    //             },
    //             body: {"user_name": chosenChar,"MBTI_to": mbti}
    //         })
    //         if(changeCharac.ok)alert("Character finish")
    //     }catch(e){
    //         setErr(e.error_detail)
    //     }
    // }

    return(
        <div>
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
        </div>
    )

}