
document.addEventListener("DOMContentLoaded",()=>{
    const inputField=document.getElementById("question")
    const btn=document.getElementById("btn1")
    const output=document.getElementById("output")

    // Regulat expressions
    let regexReplace=/(<|>)/gi
    let regexSplit=/(v=| vi\/ | \/v\/ | youtu\.be\/ | \/embed\/)/
    let regexId=/[^0-9a-z\-]/i




    btn.addEventListener("click",(e)=>{
        e.preventDefault()
        chrome.tabs.query({currentWindow:true,active:true},(tabs)=>{
            let url=tabs[0].url
            const div=document.createElement("div")
            div.className="p-4 mt-1"
            div.innerHTML=url
            output.appendChild(div)
            
            let id=url.replace(regexReplace,"").split(regexSplit)[2]
            if(id!==undefined){
                id=id.split(regexId)[0]
            }
            const div2=document.createElement("div")
            div2.className="p-4 mt-1"
            div2.innerHTML=`VideoId : <span class="text-primary font-weight-bold">${id}</span>`
            output.appendChild(div2)

        
        })

    })
})