let para = document.querySelector('p');
let compStyles = window.getComputedStyle(para);
para.textContent = 'My computed font-size is ' +
    compStyles.getPropertyValue('font-size') +
    ',\n and my computed line-height is ' +
    compStyles.getPropertyValue('line-height') +
    '.';