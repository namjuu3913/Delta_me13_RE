import { useState } from "react"
//posts param will recieve the api answer, every response will make this function run
export default function ApiPost({posts}){

    return(
        <>
        {posts.map((post, i)=>(
            post.sender=="User"?(
                <div key={i} className="humanSection">
                    <pre>{post.messages}</pre>
                </div>
            ):(
                <>
                <p className="aiIndi">AI response</p>
                <div key={i} className="AiSection">
                    <pre>{post.messages}</pre>
                </div>
                </>
            )
        )
        )}
        </>
    )
}