/************************************************************************************************************
Textarea maxlength
Copyright (C) November 2005  DTHMLGoodies.com, Alf Magne Kalleland
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
Dhtmlgoodies.com., hereby disclaims all copyright interest in this script
written by Alf Magne Kalleland.
Alf Magne Kalleland, 2010
Owner of DHTMLgoodies.com
************************************************************************************************************/
/* VARIABLES YOU COULD MODIFY */
let boxSizeArray = [15,5,5];	// Array indicating how many items there is rooom for in the right column ULs
let verticalSpaceBetweenListItems = 3;	// Pixels space between one <li> and next
										// Same value or higher as margin bottom in CSS for #dragDropContainer ul li,#dragContent li
let cloneSourceItems = false;	// Items picked from main container will be cloned(i.e. "copy" instead of "cut").
let cloneAllowDuplicates = false;	// Allow multiple instances of an item inside a small box(example: drag Student 1 to team A twice
/* END VARIABLES YOU COULD MODIFY */
let dragDropTopContainer = false;
let dragTimer = -1;
let dragContentObj = false;
let contentToBeDragged = false;	// Reference to dragged <li>
let contentToBeDragged_src = false;	// Reference to parent of <li> before drag started
let contentToBeDragged_next = false; 	// Reference to next sibling of <li> to be dragged
let destinationObj = false;	// Reference to <UL> or <LI> where element is dropped.
let dragDropIndicator = false;	// Reference to small arrow indicating where items will be dropped
let ulPositionArray = [];
let mouseoverObj = false;	// Reference to highlighted DIV
let MSIE = navigator.userAgent.indexOf('MSIE') >= 0;
let navigatorVersion = navigator.appVersion.replace(/.*?MSIE (\d\.\d).*/g,'$1')/1;
let arrow_offsetX = -5;	// Offset X - position of small arrow
let arrow_offsetY = 0;	// Offset Y - position of small arrow
if(!MSIE || navigatorVersion > 6){
	arrow_offsetX = -6;	// Firefox - offset X small arrow
	arrow_offsetY = -13; // Firefox - offset Y small arrow
}
let indicateDestinationBox = false;
function getTopPos(inputObj)
{
  var returnValue = inputObj.offsetTop;
  while((inputObj = inputObj.offsetParent) != null){
  	if(inputObj.tagName!=='HTML')returnValue += inputObj.offsetTop;
  }
  return returnValue;
}
function getLeftPos(inputObj)
{
  var returnValue = inputObj.offsetLeft;
  while((inputObj = inputObj.offsetParent) != null){
  	if(inputObj.tagName!=='HTML')returnValue += inputObj.offsetLeft;
  }
  return returnValue;
}
function cancelEvent()
{
	return false;
}
function initDrag(e)	// Mouse button is pressed down on a LI
{
	if(document.all)e = event;
	var st = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
	var sl = Math.max(document.body.scrollLeft,document.documentElement.scrollLeft);
	dragTimer = 0;
	dragContentObj.style.left = e.clientX + sl + 'px';
	dragContentObj.style.top = e.clientY + st + 'px';
	contentToBeDragged = this;
	contentToBeDragged_src = this.parentNode;
	contentToBeDragged_next = false;
	if(this.nextSibling){
		contentToBeDragged_next = this.nextSibling;
		if(!this.tagName && contentToBeDragged_next.nextSibling)contentToBeDragged_next = contentToBeDragged_next.nextSibling;
	}
	timerDrag();
	return false;
}
function timerDrag()
{
	if(dragTimer>=0 && dragTimer<10){
		dragTimer++;
		setTimeout('timerDrag()',10);
		return;
	}
	if(dragTimer===10){
		if(cloneSourceItems && contentToBeDragged.parentNode.id==='allItems'){
			newItem = contentToBeDragged.cloneNode(true);
			newItem.onmousedown = contentToBeDragged.onmousedown;
			contentToBeDragged = newItem;
		}
		dragContentObj.style.display='block';
		dragContentObj.appendChild(contentToBeDragged);
	}
}
function moveDragContent(e)
{
	if(dragTimer<10){
		if(contentToBeDragged){
			if(contentToBeDragged_next){
				contentToBeDragged_src.insertBefore(contentToBeDragged,contentToBeDragged_next);
			}else{
				contentToBeDragged_src.appendChild(contentToBeDragged);
			}
		}
		return;
	}
	if(document.all)e = event;
	var st = Math.max(document.body.scrollTop,document.documentElement.scrollTop);
	var sl = Math.max(document.body.scrollLeft,document.documentElement.scrollLeft);
	dragContentObj.style.left = e.clientX + sl + 'px';
	dragContentObj.style.top = e.clientY + st + 'px';
	if(mouseoverObj)mouseoverObj.className='dragDropBox';
	destinationObj = false;
	dragDropIndicator.style.display='none';
	if(indicateDestinationBox)indicateDestinationBox.style.display='none';
	var x = e.clientX + sl;
	var y = e.clientY + st;
	var width = dragContentObj.offsetWidth;
	var height = dragContentObj.offsetHeight;
	var tmpOffsetX = arrow_offsetX;
	var tmpOffsetY = arrow_offsetY;
	for(var no=0;no<ulPositionArray.length;no++){
		var ul_leftPos = ulPositionArray[no]['left'];
		var ul_topPos = ulPositionArray[no]['top'];
		var ul_height = ulPositionArray[no]['height'];
		var ul_width = ulPositionArray[no]['width'];
		if((x+width) > ul_leftPos && x<(ul_leftPos + ul_width) && (y+height)> ul_topPos && y<(ul_topPos + ul_height)){
			var noExisting = ulPositionArray[no]['obj'].getElementsByTagName('LI').length;
			if(noExisting<boxSizeArray[no]){
				dragDropIndicator.style.left = ul_leftPos + tmpOffsetX + 'px';
				var subLi = ulPositionArray[no]['obj'].getElementsByTagName('LI');
				var clonedItemAllreadyAdded = false;
				if(cloneSourceItems && !cloneAllowDuplicates){
					for(var liIndex=0;liIndex<subLi.length;liIndex++){
						if(contentToBeDragged.id === subLi[liIndex].id)clonedItemAllreadyAdded = true;
					}
					if(clonedItemAllreadyAdded)continue;
				}
				for(var liIndex=0;liIndex<subLi.length;liIndex++){
					var tmpTop = getTopPos(subLi[liIndex]);

				}

				if(subLi.length>0 && dragDropIndicator.style.display==='none'){
					dragDropIndicator.style.top = getTopPos(subLi[subLi.length-1]) + subLi[subLi.length-1].offsetHeight + tmpOffsetY + 'px';
					dragDropIndicator.style.display='block';
				}
				if(subLi.length===0){
					dragDropIndicator.style.top = ul_topPos + arrow_offsetY + 'px'
					dragDropIndicator.style.display='block';
				}

				if(!destinationObj)destinationObj = ulPositionArray[no]['obj'];
				mouseoverObj = ulPositionArray[no]['obj'].parentNode;
				mouseoverObj.className='mouseover';
				return;
			}
		}
	}
}
/* End dragging
Put <LI> into a destination or back to where it came from.
*/
function dragDropEnd(e)
{
	if(dragTimer===-1)return;
	if(dragTimer<10){
		dragTimer = -1;
		return;
	}
	dragTimer = -1;
	if(document.all)e = event;
	if(cloneSourceItems && (!destinationObj || (destinationObj && (destinationObj.id==='allItems' || destinationObj.parentNode.id==='allItems')))){
		contentToBeDragged.parentNode.removeChild(contentToBeDragged);
	}else{
		if(destinationObj){
			if(destinationObj.tagName==='UL'){
				destinationObj.appendChild(contentToBeDragged);
			}else{
				destinationObj.parentNode.insertBefore(contentToBeDragged,destinationObj);
			}
			mouseoverObj.className='dragDropBox';
			destinationObj = false;
			dragDropIndicator.style.display='none';
			if(indicateDestinationBox){
				indicateDestinationBox.style.display='none';
				document.body.appendChild(indicateDestinationBox);
			}
			contentToBeDragged = false;
			return;
		}
		if(contentToBeDragged_next){
			contentToBeDragged_src.insertBefore(contentToBeDragged,contentToBeDragged_next);
		}else{
			contentToBeDragged_src.appendChild(contentToBeDragged);
		}
	}
	contentToBeDragged = false;
	dragDropIndicator.style.display='none';
	if(indicateDestinationBox){
		indicateDestinationBox.style.display='none';
		document.body.appendChild(indicateDestinationBox);
	}
	mouseoverObj = false;
}
/*
Preparing data to be saved
*/
function initDragDropScript()
{
	dragContentObj = document.getElementById('dragContent');
	dragDropIndicator = document.getElementById('dragDropIndicator');
	dragDropTopContainer = document.getElementById('dragDropContainer');
	document.documentElement.onselectstart = cancelEvent;;
	var listItems = dragDropTopContainer.getElementsByTagName('LI');	// Get array containing all <LI>
	var itemHeight = false;
	for(var no=0;no<listItems.length;no++){
		listItems[no].onmousedown = initDrag;
		listItems[no].onselectstart = cancelEvent;
		if(!itemHeight)itemHeight = listItems[no].offsetHeight;
		if(MSIE && navigatorVersion<6){
			listItems[no].style.cursor='hand';
		}
	}
	var mainContainer = document.getElementById('mainContainer');
	var uls = mainContainer.getElementsByTagName('UL');
	itemHeight = itemHeight + verticalSpaceBetweenListItems;
	for(var no=0;no<uls.length;no++){
		uls[no].style.height = itemHeight * boxSizeArray[no]  + 'px';
	}

	document.documentElement.onmousemove = moveDragContent;	// Mouse move event - moving draggable div
	document.documentElement.onmouseup = dragDropEnd;	// Mouse move event - moving draggable div
	var ulArray = dragDropTopContainer.getElementsByTagName('UL');
	for(var no=0;no<ulArray.length;no++){
		ulPositionArray[no] = [];
		ulPositionArray[no]['left'] = getLeftPos(ulArray[no]);
		ulPositionArray[no]['top'] = getTopPos(ulArray[no]);
		ulPositionArray[no]['width'] = ulArray[no].offsetWidth;
		ulPositionArray[no]['height'] = ulArray[no].clientHeight;
		ulPositionArray[no]['obj'] = ulArray[no];
	}

	let teamList_height =  document.getElementById('teamList').clientHeight;
	let mainField_height =  document.getElementById('box').clientHeight;

	if (teamList_height > mainField_height){
		document.getElementById('box').style.height = teamList_height;
	}
	else {
		document.getElementById('teamList').style.height = mainField_height;
	}

}






window.onload = initDragDropScript;


