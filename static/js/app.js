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
$(document).ready(function () {
    $('.intro__inner').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        dots: true,
        arrows: true,
        fade: true
    });
});