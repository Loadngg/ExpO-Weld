// Animations
window.onload = () => window.scrollTo(0, 0);
const animItems = document.querySelectorAll('.anim-item')

if (animItems.length > 0) {
    const animOnScroll = () => {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index]
            const animItemH = animItem.clientHeight
            const animItemOffset = offset(animItem).top
            const animStart = 4

            let animItemPoint = window.innerHeight - animItemH / animStart
            if (animItemH > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart
            }

            if (window.scrollY > animItemOffset - animItemPoint && window.scrollY < animItemOffset + animItemH) {
                animItem.classList.add('show')
            }
        }
    }

    const offset = el => {
        const rect = el.getBoundingClientRect(),
            scrollLeft = window.scrollX || document.documentElement.scrollLeft,
            scrollTop = window.scrollY || document.documentElement.scrollTop
        return {
            top: rect.top + scrollTop,
            left: rect.left + scrollLeft,
        }
    }

    window.addEventListener('scroll', animOnScroll)

    setTimeout(() => {
        animOnScroll()
    }, 300)
}

// Slick
const base_config = {
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: false,
    dots: false,
    arrows: true,
    fade: false,
    infinite: true,
};

$(document).ready(function () {
    $('.intro__inner').slick({
        ...base_config,
        slidesToShow: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: false,
        fade: true,
    });
    $('.popular_products__block').slick({
        ...base_config,
        responsive: [
            {
                breakpoint: 1270,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 960,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 590,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
    $('.brands__block').slick({
        ...base_config,
        responsive: [
            {
                breakpoint: 960,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 590,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
    $('.videos__block').slick({
        ...base_config,
        slidesToShow: 3,
        responsive: [
            {
                breakpoint: 960,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 770,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
    $('.product__images').slick({
        ...base_config,
        slidesToShow: 1,
    });
});

// Accordion
$(document).ready(function () {
    $("#questions-accordion").accordionjs();
    $("#filters-accordion").accordionjs({
        closeAble: true,
        closeOther: false,
        activeIndex: false
    });
});

const filters = document.getElementById('filters-form')

function toggleFilters(event, button) {
    event.preventDefault()
    filters.classList.contains('hidden')
        ? button.innerText = "Скрыть фильтры"
        : button.innerText = "Показать фильтры"
    filters.classList.toggle('hidden')
}

// Scroll Top
const header = document.getElementById("header");
let headerH = header.clientHeight;
let scrollOffset = window.scrollY;

const scrollTopBtn = document.getElementById("up-button");
scrollTopBtn.onclick = () => window.scrollTo({top: 0, behavior: "smooth"});

checkPos(scrollOffset);

window.onscroll = () => {
    scrollOffset = window.scrollY;

    checkPos(scrollOffset);
};

function checkPos(scrollOffset) {
    scrollTopBtn.classList.toggle("hidden", scrollOffset < headerH);
}

function toggleHeader(event) {
    event.preventDefault()
    header.classList.toggle('active')
}

// Overflow
const toggleOverflowVisibility = (formId, show = true) => {
    const form = document.getElementById(formId);

    form.classList.toggle(show ? 'hidden' : 'transparent', !show)
    setTimeout(() => {
        form.classList.toggle(show ? 'transparent' : 'hidden', !show)
    }, 200)
};

// Callback Form
const toggleFormMessage = (block, message, hiddenState) => {
    block.innerText = message ? message : ""
    block.classList.toggle('hidden', hiddenState ? hiddenState : !block.innerText.trim().length);
}

const formId = 'callback'
const formBlock = document.getElementById(formId)
const form = formBlock.querySelector(`#${formId}-form`)
const formMessage = form.querySelector('.overflow__message');
const submitButton = form.querySelector('.button');
const overflowMessage = "overflow__message"
const overflowMessageSuccess = `${overflowMessage}--success`
const overflowMessageError = `${overflowMessage}--error`

form.addEventListener('submit', function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    formMessage.classList.remove(overflowMessageError)
    formMessage.classList.remove(overflowMessageSuccess)
    toggleFormMessage(formMessage, "Отправка...", false)
    submitButton.classList.toggle('disabled', true);

    fetch(this.action, {method: 'POST', body: formData, credentials: 'include'})
        .then(response => response.json())
        .then(data => {
            if (data.error_message.length > 0) {
                toggleFormMessage(formMessage, data.error_message)
                formMessage.classList.add(overflowMessageError)
                submitButton.classList.toggle('disabled', false);
            }

            if (!data.success) return;
            if (data.success_message && data.error_message.length === 0) {
                toggleFormMessage(formMessage, data.success_message)
                if (formMessage.classList.contains(overflowMessageError)) {
                    formMessage.classList.remove(overflowMessageError)
                }
                formMessage.classList.add(overflowMessageSuccess)

                setTimeout(() => {
                    toggleOverflowVisibility(formId, false)
                    formMessage.classList.remove(overflowMessageError)
                    formMessage.classList.remove(overflowMessageSuccess)
                    submitButton.classList.toggle('disabled', false);
                    form.reset()
                    toggleFormMessage(formMessage)
                }, 3000)

                return;
            }
            window.location.href = data.redirect_url;
        })
        .catch(error => {
            console.error('Error:', error);
            toggleFormMessage(formMessage, 'Произошла ошибка при обработке запроса')
            formMessage.classList.add(overflowMessageError)
        });
});