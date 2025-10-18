import "../App.css"
export default function ErrorDisplay({error}){
    return(
        <div className="backGrandScrollOverf">
            <p>Something is wrong: {error}</p>
        </div>
    )
}