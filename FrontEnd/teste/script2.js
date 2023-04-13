function slideCards(container) {
    const cards = container.querySelectorAll('.card');
    let currentPosition = 0;
    const cardWidth = cards[0].offsetWidth;
    const numCards = cards.length;
    
    container.style.width = `${cardWidth*numCards}px`;
    
    function moveCards(position) {
      container.style.transform = `translateX(-${position*cardWidth}px)`;
    }
    
    // Next button click
    document.querySelector('.next').addEventListener('click', () => {
      currentPosition = Math.min(currentPosition + 1, numCards-1);
      moveCards(currentPosition);
    });
    
    // Prev button click
    document.querySelector('.prev').addEventListener('click', () => {
      currentPosition = Math.max(currentPosition - 1, 0);
      moveCards(currentPosition);
    });
  }

const cardSlider = document.querySelector('.card-slider');
slideCards(cardSlider);