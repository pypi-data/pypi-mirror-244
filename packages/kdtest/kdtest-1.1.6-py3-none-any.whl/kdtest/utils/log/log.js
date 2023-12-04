function boxFold(element){
    foldSwitch = Boolean(element.getAttribute("fold"));
    fatherElement = element.parentNode; // 父级节点
    sonElement = fatherElement.querySelector('.case-result-box');  // 结果盒子
    arrowsElement = fatherElement.querySelector('.case-title-box .arrows')  // 展开箭头
    if (foldSwitch){
        element.removeAttribute('fold');
        sonElement.style.display = "block";
        arrowsElement.style = "transform: rotate(45deg) translateY(-50%); transform-origin: right top;";
    } else {
        element.setAttribute("fold", "fold");
        sonElement.style.display = "none";
        arrowsElement.style = "transform: rotate(-45deg) translateY(-50%);";
    }
}