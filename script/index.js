const duration = 1500
const interval = 10
const API_PROGETTI = "https://raw.githubusercontent.com/lucx-albx/Progetti/main/Progetti.json"

let isAnimationRunning = false
let isAnimationRunningPercentuale = false

const apri_menu =()=>{
    let controlla = document.querySelector(".tipi-sezioni")
    let altezza = -130

    controlla.style.top = altezza + 'px'

    let id = setInterval(frame, 1)

    if(controlla.classList.contains("not-visible"))
        controlla.classList.remove("not-visible")
    else
        controlla.classList.add("not-visible")

    function frame(){
        if (altezza >= 68) {
            clearInterval(id)
        } else {
            altezza += 6
            controlla.style.top = altezza + 'px'
        }
    
    }
    
}

const checkScreenWidth =()=> {
    let controlla = document.querySelector(".tipi-sezioni")
    let descrizione = document.querySelector(".desc")
    let servizi = document.querySelector(".ser")

    if (window.innerWidth >= 768) {
        controlla.classList.add("visible-tel")
        descrizione.classList.add("posiziona-verticale-centrale")
        servizi.classList.add("posiziona-verticale-centrale")        
    } else {
        controlla.classList.remove("visible-tel")
        servizi.classList.remove("posiziona-verticale-centrale")
        descrizione.classList.remove("posiziona-verticale-centrale")
    }

}

const anima_numero_progetti =(finalNumber, numero)=> {
    let currentNumber = 0
    const increment = finalNumber / (duration / interval)

    const intervalId = setInterval(() => {
        currentNumber += increment
        numero.textContent = Math.round(currentNumber)

        if (currentNumber >= finalNumber) {
            numero.textContent = finalNumber
            clearInterval(intervalId)
        }
    }, interval)
}

class card_progetti{
    crea(nome, desc, link){
        return (
                `<div class="col-xl-5 col-lg-5 col-md-5 col-10 card-progetti" data-aos="zoom-in" data-aos-offset="10" data-aos-easing="ease-in-sine">
                        <h2 class="text-center testo-progetti-tit">${nome}</h2>
                        <p class="testo-desc-proj mt-2">
                            ${desc}
                        </p>
                        
                        <div class="bottom-card-proj">
                            <a href="${link}" target="_blank" class="more mt-2 d-flex justify-content-start align-items-center">Esplora <svg class="centra-freccia" height="20" width="25" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75" stroke-linejoin="round" stroke-linecap="round"></path></svg></a>
                        </div>
                </div>`
            )
    }

    crea_python(nome, desc, link){
        return (
            `<div class="col-xl-5 col-lg-5 col-md-5 col-10 card-progetti" data-aos="zoom-in" data-aos-offset="10" data-aos-easing="ease-in-sine">
                    <h2 class="text-center testo-progetti-tit">${nome}</h2>
                    <p class="testo-desc-proj mt-2">
                        ${desc}
                    </p>
                    <a href="${link}" class="more d-flex justify-content-start align-items-center" download>Scarica <svg class="centra-freccia" height="20" width="25" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75" stroke-linejoin="round" stroke-linecap="round"></path></svg></a>
            </div>`
        )
    }
}

const carica_progetti =(blocco_selezionato = "")=>{
    blocco_selezionato = blocco_selezionato !== "" ? blocco_selezionato : "sw"

    let main_proj = document.querySelector(".all-proj")
    let blocco = document.querySelector("." + blocco_selezionato)
    let lista_blocchi_progetti = ['wa', 'sw', 'ap']
    let insert = ""

    //Aggiungo stile al blocco selezionato
    lista_blocchi_progetti.map((elem)=>{
        document.querySelector("." + elem).style.border = "none"
    })

    blocco.style.border = "2.5px solid #e2af27"

    fetch(API_PROGETTI)
    .then(testo=>testo.json())
    .then((data)=>{
        try {
            if(blocco_selezionato === "wa"){
                //carico info webapp
                data.Web_app.map((elem, i)=>{
                    insert += new card_progetti().crea(elem.nome, elem.descrizione, elem.link)
                })

                main_proj.innerHTML = insert
            } else if(blocco_selezionato === "sw"){
                //carico info siti web
                insert = ""

                data.Siti_web.map((elem, i)=>{
                    insert += new card_progetti().crea(elem.nome, elem.descrizione, elem.link)
                })

                main_proj.innerHTML = insert
            } else if(blocco_selezionato === "ap"){
                //carico info python
                insert = ""

                data.Python_progetti.map((elem, i)=>{
                    insert += new card_progetti().crea_python(elem.nome, elem.descrizione, elem.link, "100")
                })

                main_proj.innerHTML = insert
            }
        } catch(err){}
    })
    
}

const carica_percentuali =()=>{
    let progressHtml = document.querySelector(".completamento1")
    let progressCss = document.querySelector(".completamento2")
    let progressJs = document.querySelector(".completamento3")
    let progressReact = document.querySelector(".completamento4")
    let progressPython = document.querySelector(".completamento5")
    let progressC = document.querySelector(".completamento6")
    let progressBash = document.querySelector(".completamento7")
    let progressSql = document.querySelector(".completamento8")
    let progressFirebase = document.querySelector(".completamento9")
    let progressPhp = document.querySelector(".completamento10")
    
    progressHtml.classList.add("animate")
    progressCss.classList.add("animate")
    progressJs.classList.add("animate")
    progressReact.classList.add("animate")
    progressPython.classList.add("animate")
    progressC.classList.add("animate")
    progressBash.classList.add("animate")
    progressSql.classList.add("animate")
    progressFirebase.classList.add("animate")
    progressPhp.classList.add("animate")
}

const scrollToTop =()=> {
    const topElement = document.documentElement;
    topElement.scrollIntoView({
        behavior: 'smooth'
    })
}

checkScreenWidth()
window.addEventListener('resize', checkScreenWidth)

window.addEventListener('scroll', () => {
    try{
        const section = document.getElementById('animazionePercentuale')
        const sectionTop = section.getBoundingClientRect().top

        if (sectionTop <= window.innerHeight / 1.2 && !isAnimationRunningPercentuale) {
            carica_percentuali()

            isAnimationRunningPercentuale = true
        }
    } catch(err){}

})

window.addEventListener('scroll', () => {
    try{
        const section = document.getElementById('animazioneNumeri')
        const sectionTop = section.getBoundingClientRect().top

        if (sectionTop <= window.innerHeight / 2 && !isAnimationRunning) {
            anima_numero_progetti(14, document.querySelector(".progetti-pubblicati-numero"))
            anima_numero_progetti(32, document.querySelector(".progetti-sviluppati-numero"))
            anima_numero_progetti(7, document.querySelector(".progetti-iconici-numero"))
            anima_numero_progetti(12, document.querySelector(".progetti-webapp-numero"))

            isAnimationRunning = true
        }

    } catch(err){}
})

window.addEventListener('load', () => {
    AOS.init({
        duration: 850,
        easing: "ease-in-out",
        once: true,
        mirror: false
    })

    carica_progetti('wa')
})
