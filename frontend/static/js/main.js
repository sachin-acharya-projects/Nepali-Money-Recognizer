const uploadBtn = document.getElementById("upload-btn")
const classifyBtn = document.getElementById("classify-btn")
const fileInput = document.getElementById("upload-input")
const form = document.getElementById("form")

const previewImageContainer = document.querySelector(".image-preview-container")
const previewImage = document.querySelector(".preview-img")
const imageText = document.querySelector(".image-text")

uploadBtn.addEventListener("click", () => {
    fileInput.click()
})

fileInput.addEventListener("change", (e) => {
    if (!fileInput.files.length) {
        previewImageContainer.classList.remove("active")
        previewImage.src = ""
        classifyBtn.classList.remove("active")
    }

    previewImageContainer.classList.remove("active")
    classifyBtn.classList.remove("active")
    const imageSrc = URL.createObjectURL(fileInput.files[0])

    setTimeout(() => {
        previewImage.src = imageSrc
        imageText.innerHTML = "Press Classify"
        previewImageContainer.classList.add("active")
        setTimeout(() => {
            classifyBtn.classList.add("active")
        }, 250)
    }, 350)
})

const money_list = {
    one: 1,
    two: 2,
    five: 5,
    ten: 10,
    twenty: 20,
    fifty: 50,
    hundred: 100,
    "five hundred": 500,
    thousand: 1000,
}

form.addEventListener("submit", function (e) {
    e.preventDefault()
    const formData = new FormData(this)

    fetch("/", {
        method: "POST",
        body: formData,
    })
        .then((data) => data.json())
        .then((data) => {
            if (!data["status"]) alert(data["message"])
            if ("classname" in data)
                imageText.innerText =
                    "Rupee " + money_list[data["classname"].toLowerCase()]
        })
})
