
document.addEventListener("DOMContentLoaded",()=>{

    const inputField=document.getElementById("question")
    const btn=document.getElementById("btn1")
    const output=document.getElementById("output")
    // Regulat expressions
    let regexReplace=/(<|>)/gi
    let regexSplit=/(v=| vi\/ | \/v\/ | youtu\.be\/ | \/embed\/)/
    let regexId=/[^0-9a-z\-]/i

    const timeConvertor=(seconds)=>{
        let str=""
        let hrs=parseInt(seconds/3600)
        let min_sec=seconds%3600
        let min=parseInt(min_sec/60);
        let sec=min_sec%60
        str=hrs+":"+min+":"+sec.toFixed(2)
        return str
    }
    
    
    
    
    

const  displayData=(data)=>{
    output.innerHTML=""

    const ul=document.createElement("ul")
    ul.className="list-group"
    data.forEach(ele=>{
    
        const li=document.createElement("li")
        li.className="list-group-item list-group-item-action"
        li.innerHTML=`

                        <div class="row">
                            <div class="col-md-1"></div>
                            <div class="col-md-10"><span class="text-primary font-weight-bold">Text</span>: <span class="font-weight-bold">${ele.text}</span> </div>
                            <div class="col-md-1"></div>
                        </div> 
                        <div class="row">
                            <div class="col-md-1"></div>
                            <div class="col-sm-5"><span class="text-primary font-weight-bold">Start</span>: <span class="font-weight-bold">${timeConvertor(ele.start)}</span> </div>
                            <div class="col-sm-5"><span class="text-primary font-weight-bold">Duration</span>: <span class="font-weight-bold">${timeConvertor(ele.duration)}</span>  </div>
                            <div class="col-md-1"></div>
                        </div>
                        
        `
        ul.appendChild(li)
    })
    output.appendChild(ul)
    
}



const getResponse=async(video_id,userQuestion)=>{
    const formdata=new FormData()
    formdata.append("video_id",video_id)
    formdata.append("question",userQuestion)
    const options={
        body:formdata,
        method:"POST"
    }
    try{
        const res=await fetch("http://127.0.0.1:5000/response",options)
        const data=await res.json()
        console.log(data)
        displayData(data)
    }
    catch(err){
        console.log(err)
    }
}


    


    btn.addEventListener("click",(e)=>{
        e.preventDefault()

        let userInput=inputField.value
        let id;
        chrome.tabs.query({currentWindow:true,active:true},(tabs)=>{
            let url=tabs[0].url
            // const div=document.createElement("div")
            // div.className="p-4 mt-1"
            // div.innerHTML=url
            // output.appendChild(div)
            
            id=url.replace(regexReplace,"").split(regexSplit)[2]
            if(id!==undefined){
                id=id.split(regexId)[0]
            }
            getResponse(id,userInput)
            const div2=document.createElement("div")
            div2.className="p-4 mt-1 text-center"
            div2.innerHTML=`VideoId : <span class="text-primary font-weight-bold">${id}</span>
            <h4>loading ... </h4>`
            output.appendChild(div2)
        })
        
    })


})


