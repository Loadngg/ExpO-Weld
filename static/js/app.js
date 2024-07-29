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