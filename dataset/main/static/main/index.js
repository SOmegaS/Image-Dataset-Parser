const addButton = document.querySelector('.form__add-button');
const submitButton = document.querySelector('.form__submit-button');
const inputForm = document.querySelector('.form');
const sectionInputs = document.querySelector('.form__inputs-container');
const containerItem = document.querySelector('#form__container-item').content;
const sectionResult = document.querySelector('.form__result-container');
const resultItem = document.querySelector('#form__result-item').content;

addButton.addEventListener('click', () => {
    const inputsItem = containerItem.querySelector('.form__container-item').cloneNode(true);
    const deleteButton = inputsItem.querySelector('.form__delete-button');
    deleteButton.addEventListener('click', () => {
        inputsItem.remove();
        toggleButtonState([], submitButton);
    })
    sectionInputs.append(inputsItem);
    enableValidation(validationParameters, inputsItem);
})

function checkResponse(res) {
    if (res.ok) {
        return res.json();
    }
    return Promise.reject(`Ошибка ${res.status}`);
}

function renderLoading(isLoading) {
    const deleteButtons = Array.from(document.querySelectorAll('.form__delete-button'));
    if (isLoading) {
        submitButton.textContent = "In progress...";
        deleteButtons.forEach((buttonElement) => {
            buttonElement.setAttribute("disabled", "disabled");
        })
        addButton.setAttribute("disabled", "disabled");
    } else {
        submitButton.textContent = "Submit";
        deleteButtons.forEach((buttonElement) => {
            buttonElement.removeAttribute("disabled", "disabled");
        })
    }
}

function createDownloader(obj) {  // obj = {array: [{link: ..., name: ...} ...]}
    (obj.array).forEach((elem) => {
        const item = resultItem.querySelector('.form__result-item').cloneNode(true);
        const currentLink = item.querySelector('.form__result-link');
        currentLink.download = elem.link;
        currentLink.textContent = elem.name;
        sectionResult.append(item);
    })
}

inputForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const classArray = Array.from(document.querySelectorAll('input[name="classname"]')).map((item) => {
        return item.value;
    })
    const countArray = Array.from(document.querySelectorAll('input[name="count"]')).map((item) => {
        return item.value;
    })
    renderLoading(true);
    //createDownloader({array: [{link: "./images/Vector.svg", name: "First class"}]})  //demo
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            class: classArray,
            count: countArray
        })
    })
    .then(checkResponse)
    .then((res) => {
        createDownloader(res)
    })
    .finally(() => renderLoading(false))
    .catch((err) => console.log(err));
})

// validation

const validationParameters = {
    formSelector: '.form',
    inputSelector: '.form__input',
    submitButtonSelector: '.form__submit-button',
    inputErrorClass: 'form__input_error',
    errorClass: 'form__form-error_active'
};

const showInputError = (inputElement, errorMessage, obj, inpItem) => {
    const errorElement = inpItem.querySelector(`.${inputElement.id}-error`);
    console.log(errorElement);
    inputElement.classList.add(obj.inputErrorClass);
    errorElement.textContent = errorMessage;
    errorElement.classList.add(obj.errorClass);
};

const hideInputError = (inputElement, obj, inpItem) => {
    const errorElement = inpItem.querySelector(`.${inputElement.id}-error`);
    inputElement.classList.remove(obj.inputErrorClass);
    errorElement.classList.remove(obj.errorClass);
    errorElement.textContent = '';
};

const toggleButtonState = (inputList, buttonElement) => {
    if (hasInvalidInput(inputList) || inputList.length === 0) {
        buttonElement.setAttribute("disabled", "disabled");
    } else {
        buttonElement.removeAttribute("disabled", "disabled");
    }
};

const checkInputValidity = (inputElement, obj, inpItem) => {
    if (!inputElement.validity.valid) {
        showInputError(inputElement, inputElement.validationMessage, obj, inpItem);
    } else {
        hideInputError(inputElement, obj, inpItem);
    }
};

const setEventListeners = (formElement, obj, inpItem) => {
    const inputList = Array.from(inpItem.querySelectorAll(obj.inputSelector));

    const buttonElement = formElement.querySelector(obj.submitButtonSelector);

    toggleButtonState(inputList, buttonElement);
    inputList.forEach((inputElement) => {
        inputElement.addEventListener('input', function () {
            checkInputValidity(inputElement, obj, inpItem);
            toggleButtonState(inputList, buttonElement);
        });
    });
};

const enableValidation = (obj, inpItem) => {
    const form = document.querySelector(obj.formSelector);
    setEventListeners(form, obj, inpItem);
};


const hasInvalidInput = (inputList) => {
    return inputList.some((inputElement) => {
        return !inputElement.validity.valid;
    })
};