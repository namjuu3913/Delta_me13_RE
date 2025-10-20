export default function SetMbti({chosenChar, checkLock1, setErr}){
    // set MBTI
    const [mbti, setmbti] = useState("")
    const setMBTI = async ()=>{
        try{
            const changeCharac = await fetch(`${api}change_character_personality/`, {
                method: PATCH,
                headers: {
                    "Content-Type": "application/json"
                },
                body: {"user_name": chosenChar,"MBTI_to": mbti}
            })
            let res
            if(changeCharac.ok){
                res = await changeCharac.json() 
                if(res.is_normal&&res.is_changed)
                    checkLock1(true)
            }
        }catch(e){
            setErr(e.message.error_detail)
        }
    }
    return(
        <div>
            <form onSubmit={setMBTI}>
                Set the MBTI for an AI
                <input value={mbti} onChange={(e)=>setmbti(e.target.value)}></input>
                <button type="submit">Submit MBTI</button>
            </form>
        </div>
    )
}