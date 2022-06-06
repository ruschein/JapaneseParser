
(function () {
	// constructor
	const Highlight = function(characters, highlightClass, otherClasses, unwantedTags, tagFilter) {
		this.characters = characters;
		this.highlightClass = highlightClass;
		this.otherClasses = otherClasses;
		this.unwantedTags = unwantedTags;
		this.tagFilter = tagFilter;
		this.highlighted = [];
	}

	Highlight.prototype = {
		highlighter: function (tags) {
			const regex = new RegExp(`[${this.characters.join('')}]`, "g");

			const span = document.createElement("span");
			span.classList.add(this.highlightClass);
			this.otherClasses.forEach(className => span.classList.add(className));

			Array.from(tags).filter(tag => tag.textContent.match(regex)?.length > 0 && this.tagValidation(tag))
				.forEach(node => this.highlighted = this.highlighted.concat(replaceMatchesWithElem(node, regex, span)));
			
		},

		// check if given tag is of interest
		tagValidation: function (tag) { return !this.unwantedTags.includes(tag.localName) && textChildNodes(tag).length > 0 && !(this.hasDirectChildHighlighted(tag) || tag.classList.contains(this.highlightClass)) && this.tagFilter(tag) },

		// check if a tag has already highlighted nodes
		hasDirectChildHighlighted: function (tag) {
			for (let child of tag.children) {
				if (Array.from(child.classList).includes(this.highlightClass))
					return true;
			}
			return false;
		},

		highlightedSet: function () { return [...new Set(this.highlighted)] },

		size: function () { return this.highlightedSet().length; }
	}

	// Aux functions

	// check if node has children with text
	const textChildNodes = obj => Array.from(obj.childNodes).filter(node => node.nodeName === "#text");
    
	// Generated

	const vocabs = new Map();
	vocabs.set('日', ['ひ', 'Sun']);
	vocabs.set('日本', ['にほん', 'Japan']);
	vocabs.set('食', ['た', 'Food']);
	vocabs.set('食べる', ['たべる', 'To Eat']);
	vocabs.set('人', ['ひと', 'Person']);
	vocabs.set('私', ['わたし', 'I']);
  
function isKanji(ch) {
    return (("\u4e00" <= ch) && (ch <= "\u9faf"));
}


function matchVocab(text) {
  /*[日,本,人] = matchVocab("さくらは日本人です。") */
  var match, split, vocab, pos;
  match = [];
  split = [];
  pos = 0;
  kanaRoot = 0;
  vocabRoot = 0;
  vocab = "";
  kanaTail = "";
  kanaHead = "";
  //console.log("text='"+text+"'");
  for (var ch, _pj_c = 0, _pj_a = text, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
    ch = _pj_a[_pj_c];

    if (isKanji(ch)) {
      //console.log('。' + vocab + ch+ '。');
	  //console.log("kanjiTail="+kanaTail);
	  if (vocab == "") {
		  vocabRoot = pos;
		  kanaTail = "";
	  }
	  if (kanaTail != "") {
		if (vocab != "") {
			// Already vocab there but it has ended in kanji sequence.
			match = match.concat([vocab]);
			if (vocabRoot > kanaRoot) {
 				split = split.concat([text.slice(kanaRoot, vocabRoot-kanaRoot)]);
			} else { // No leading kana.
				split = split.concat(['']);
				//split = split.concat([kanaTail]);
			}
      		vocab = "";
			vocabRoot = pos;
			kanaRoot = pos - kanaTail.length;
			kanaHead = kanaTail; //kanaTail = "";
	 	}
	  }
	  if (vocabs.has(vocab + ch)) {
        vocab = vocab + ch;
      } else {
		if (vocab != "") {
			// Already vocab there but it has ended in kanji sequence.
			match = match.concat([vocab]);
			kanaRoot -= kanaTail.length;
			if (vocabRoot > kanaRoot) {
 				split = split.concat([text.slice(kanaRoot, vocabRoot-kanaRoot)]);
			} else {
				split = split.concat([""]);
			}
      		vocab = ch;
			vocabRoot = pos;
			kanaRoot = pos - kanaTail.length;
			kanaTail = "";
	 	}
      }
    } else { // Kana
		// 食べ ない, 食べ た, 食べ なかった
		//if (ch != '\n') console.log("ch='"+ch+"'");
		kanaTail = kanaTail+ch;
		//if (ch != '\n') console.log("kanaTail='"+kanaTail+"'");
		if (ch == 'る') {
			// Verb ?
			console.log("ru:"+vocab + kanaTail);
			if (vocab != "") {
				if (vocabs.has(vocab + kanaTail)) {
					vocab = vocab + kanaTail
					match = match.concat([vocab]);
					if (vocabRoot > kanaRoot) {
						split = split.concat([text.slice(kanaRoot, vocabRoot-kanaRoot+1)]);
					} else { // No leading kana.
						split = split.concat(['']);
					}
					vocab = "";
					kanaTail = "";
					vocabRoot = pos+1;
					kanaRoot = pos+1;
				}
			}
		} else {
			if ((vocab != "") && (kanaTail.length > 1)) {
				// Give up for parsing trail.
				match = match.concat([vocab]);
				if (vocabRoot > kanaRoot) {
					split = split.concat([text.slice(kanaRoot, vocabRoot-kanaRoot)+kanaHead]);
				} else { // No leading kana.
					split =split.concat(['']);
				}
				vocabRoot = pos+1 - kanaTail.length;
				kanaRoot = pos+1 - kanaTail.length + kanaHead.length;
				kanaHead = "";
				vocab = "";
				kanaTail = "";
			}
 		}
    }
	pos += 1;
  }
  split = split.concat([text.slice(kanaRoot)]);
  //console.log(split);
  return [match, split];
}
  
	  // Generated>
	/**/

	// replace a matching regex in a text node with a document element, preserving everything else, even other 
	// none text node siblings from that text node (the parent node must have atleast one text node as a childNode)
	const replaceMatchesWithElem = (parentNode, regex, elem) => {
		let allMatches = [];
		
		textChildNodes(parentNode).forEach(node => {
			const fragment = document.createDocumentFragment();
			// textContent = "さくらは日本人です。"
			// split = [さくらは,",です]
			// matches = [日本,人]
			const matchesSplit = matchVocab(node.textContent);
			const matches = matchesSplit[0];
			const split   = matchesSplit[1];
			if (matches.length > 0) {
				console.log("'"+node.textContent+"'");
				console.log(matches);
				console.log(split); 
				split.forEach((content, i) => {
					fragment.appendChild(document.createTextNode(content)); // Stuff between kanji.
					if (i !== split.length-1) {
						const clone = elem.cloneNode(true);
						clone.appendChild(document.createTextNode(matches[i]));
						fragment.appendChild(clone);
					}
				});
				node.parentElement.replaceChild(fragment, node);
				allMatches = allMatches.concat(matches);
			}
		});

		return allMatches;
	}

	window.Highlight = Highlight;
}());