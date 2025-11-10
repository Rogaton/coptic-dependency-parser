%******************************************************************************
% COPTIC_DEPENDENCY_RULES.PL - Prolog Dependency Grammar for Coptic
%******************************************************************************
%
% This module demonstrates the adaptation from DCG (DETECT5.PRO style)
% to modern dependency grammar formalism.
%
% PARADIGM SHIFT:
%   DCG:         sentence --> NP, VP.  (hierarchical constituents)
%   Dependency:  dep(verb, subject, nsubj).  (head-dependent relations)
%
% Based on Universal Dependencies annotation scheme adapted for Coptic
% linguistic patterns (VSO word order, tripartite sentences, etc.)
%
% Author: Adapted from DETECT5.PRO (André Linden, 1989-91)
% Date: 2025
%
%******************************************************************************

:- module(coptic_dependency_rules, [
    dependency_pattern/3,
    validate_dependency/4,
    suggest_parse/3,
    apply_dependency_rules/3
]).

:- ensure_loaded(coptic_lexicon).

%******************************************************************************
% CORE DEPENDENCY PATTERNS
%******************************************************************************

% Pattern 1: VSO Transitive Sentence
% Example: ⲥⲱⲧⲙ ⲡⲣⲱⲙⲉ ⲡϣⲁϫⲉ (hear the-man the-word = "The man hears the word")
%
% Dependency structure:
%   ⲥⲱⲧⲙ (VERB, root)
%   ├── ⲡⲣⲱⲙⲉ (NOUN, nsubj)
%   └── ⲡϣⲁϫⲉ (NOUN, obj)
%
dependency_pattern(vso_transitive,
    Words,
    [dep(Subj, SubjPOS, SIdx, Verb, VIdx, nsubj),
     dep(Obj, ObjPOS, OIdx, Verb, VIdx, obj)]) :-
    % Verb at position VIdx
    nth1(VIdx, Words, word(Verb, VerbPOS, _)),
    member(VerbPOS, ['VERB', 'AUX']),

    % Subject at position SIdx
    nth1(SIdx, Words, word(Subj, SubjPOS, _)),
    member(SubjPOS, ['NOUN', 'PRON', 'PROPN']),

    % Object at position OIdx
    nth1(OIdx, Words, word(Obj, ObjPOS, _)),
    member(ObjPOS, ['NOUN', 'PRON', 'PROPN']),

    % VSO word order constraint (crucial for Coptic!)
    VIdx < SIdx,
    SIdx < OIdx,

    % Verify verb is transitive
    is_transitive(Verb).

% Pattern 2: VS Intransitive Sentence
% Example: ⲃⲱⲕ ⲡⲣⲱⲙⲉ (go the-man = "The man goes")
%
dependency_pattern(vs_intransitive,
    Words,
    [dep(Subj, SubjPOS, SIdx, Verb, VIdx, nsubj)]) :-
    % Verb
    nth1(VIdx, Words, word(Verb, VerbPOS, _)),
    member(VerbPOS, ['VERB', 'AUX']),

    % Subject
    nth1(SIdx, Words, word(Subj, SubjPOS, _)),
    member(SubjPOS, ['NOUN', 'PRON', 'PROPN']),

    % VS word order
    VIdx < SIdx,

    % Verify verb is intransitive
    is_intransitive(Verb).

% Pattern 3: Tripartite Nominal Sentence
% Example: ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ (I am the-god = "I am God")
%
% Structure: Subject + Copula + Predicate
% In UD: Predicate is head, Subject and Copula depend on it
%
%   ⲡⲛⲟⲩⲧⲉ (NOUN, root)
%   ├── ⲁⲛⲟⲕ (PRON, nsubj)
%   └── ⲡⲉ (AUX, cop)
%
dependency_pattern(tripartite,
    Words,
    [dep(Subj, SubjPOS, SIdx, Pred, PIdx, nsubj),
     dep(Cop, 'AUX', CIdx, Pred, PIdx, cop)]) :-
    % Subject (first position, typically)
    nth1(SIdx, Words, word(Subj, SubjPOS, _)),
    member(SubjPOS, ['NOUN', 'PRON', 'PROPN']),

    % Copula (ⲡⲉ, ⲧⲉ, ⲛⲉ)
    nth1(CIdx, Words, word(Cop, 'AUX', _)),
    member(Cop, ['ⲡⲉ', 'ⲧⲉ', 'ⲛⲉ']),

    % Predicate (nominal or adjectival)
    nth1(PIdx, Words, word(Pred, PredPOS, _)),
    member(PredPOS, ['NOUN', 'ADJ', 'PROPN']),

    % Typical order: S - Cop - Pred (but can vary)
    SIdx < PIdx,

    % Gender/number agreement between copula and predicate
    copula_agrees_with_predicate(Cop, Pred).

% Pattern 4: Converted Tripartite (Predicate-Subject-Copula)
% Example: ⲡⲛⲟⲩⲧⲉ ⲁⲛⲟⲕ ⲡⲉ (God I am = "I am God" - emphatic)
%
dependency_pattern(tripartite_converted,
    Words,
    [dep(Subj, SubjPOS, SIdx, Pred, PIdx, nsubj),
     dep(Cop, 'AUX', CIdx, Pred, PIdx, cop)]) :-
    nth1(PIdx, Words, word(Pred, PredPOS, _)),
    member(PredPOS, ['NOUN', 'ADJ', 'PROPN']),

    nth1(SIdx, Words, word(Subj, SubjPOS, _)),
    member(SubjPOS, ['NOUN', 'PRON', 'PROPN']),

    nth1(CIdx, Words, word(Cop, 'AUX', _)),
    member(Cop, ['ⲡⲉ', 'ⲧⲉ', 'ⲛⲉ']),

    % Converted order: Pred before Subj
    PIdx < SIdx,

    copula_agrees_with_predicate(Cop, Pred).

% Pattern 5: Determiner + Noun
% Example: ⲡⲣⲱⲙⲉ (the-man)
%
% In Coptic, articles often attach as prefixes, but in tokenized form:
%   ⲡⲣⲱⲙⲉ
%   ├── ⲡ (DET, det)
%
dependency_pattern(determiner_noun,
    Words,
    [dep(Det, 'DET', DIdx, Noun, NIdx, det)]) :-
    nth1(DIdx, Words, word(Det, 'DET', _)),
    nth1(NIdx, Words, word(Noun, 'NOUN', _)),

    % Determiner precedes noun in Coptic
    DIdx < NIdx,

    % Adjacent or nearly adjacent
    NIdx - DIdx =< 2,

    % Gender agreement
    determiner_gender_agrees(Det, Noun).

% Pattern 6: Adjective Modification
% Example: ⲡⲣⲱⲙⲉ ⲛⲁⲛⲟⲩϥ (the-man good = "the good man")
%
% In Coptic, adjectives typically follow nouns
%   ⲣⲱⲙⲉ (NOUN)
%   └── ⲛⲁⲛⲟⲩϥ (ADJ, amod)
%
dependency_pattern(noun_adjective,
    Words,
    [dep(Adj, 'ADJ', AIdx, Noun, NIdx, amod)]) :-
    nth1(NIdx, Words, word(Noun, 'NOUN', _)),
    nth1(AIdx, Words, word(Adj, 'ADJ', _)),

    % Coptic: Adjective follows noun (typically)
    NIdx < AIdx,

    % Should be adjacent or nearly so
    AIdx - NIdx =< 2,

    % Gender/number agreement
    adjective_agrees(Adj, Noun).

% Pattern 7: Prepositional Phrase
% Example: ϩⲛ ⲧⲡⲟⲗⲓⲥ (in the-city)
%
%   ⲧⲡⲟⲗⲓⲥ (NOUN, head in larger structure)
%   ├── ϩⲛ (ADP, case)
%
dependency_pattern(prepositional_phrase,
    Words,
    [dep(Prep, 'ADP', PIdx, Noun, NIdx, case)]) :-
    nth1(PIdx, Words, word(Prep, 'ADP', _)),
    nth1(NIdx, Words, word(Noun, NounPOS, _)),
    member(NounPOS, ['NOUN', 'PRON', 'PROPN']),

    % Preposition before noun
    PIdx < NIdx,

    % Adjacent
    NIdx - PIdx =< 2.

% Pattern 8: Conjunction
% Example: ⲡⲣⲱⲙⲉ ⲙⲛ ⲧⲉϣⲓⲙⲉ (the-man and the-woman)
%
dependency_pattern(coordination,
    Words,
    [dep(Conj, 'CCONJ', CIdx, Head, HIdx, cc),
     dep(Coord2, Coord2POS, C2Idx, Head, HIdx, conj)]) :-
    nth1(HIdx, Words, word(Head, HeadPOS, _)),
    member(HeadPOS, ['NOUN', 'VERB', 'ADJ']),

    nth1(CIdx, Words, word(Conj, 'CCONJ', _)),

    nth1(C2Idx, Words, word(Coord2, Coord2POS, _)),
    Coord2POS = HeadPOS,  % Same POS as head

    % Order: Head < Conj < Coord2
    HIdx < CIdx,
    CIdx < C2Idx.

%******************************************************************************
% LAYTON GRAMMAR PATTERNS
%******************************************************************************

% Pattern 9: Perfective Conjugation (Layton Lesson 8, §58-60)
% Example: ⲁϥⲃⲱⲕ (a-f-bwk = "he went")
% Structure: Conjugation base (ⲁ) + Subject pronoun (ϥ) + Infinitive (ⲃⲱⲕ)
%
% Dependency:
%   ⲃⲱⲕ (VERB, root)
%   ├── ⲁ (AUX, aux) - perfective marker
%   └── ϥ (PRON, nsubj) - subject pronoun
%
dependency_pattern(perfective,
    Words,
    [dep(Aux, 'AUX', AIdx, Verb, VIdx, aux),
     dep(Pron, 'PRON', PIdx, Verb, VIdx, nsubj)]) :-
    % Auxiliary (perfective marker ⲁ)
    nth1(AIdx, Words, word(Aux, 'AUX', _)),
    member(Aux, ['ⲁ', 'ⲙⲡ']),  % ⲁ (affirmative), ⲙⲡ (negative)

    % Pronominal subject
    nth1(PIdx, Words, word(Pron, 'PRON', _)),
    member(Pron, ['ⲓ', 'ⲕ', 'ⲧⲉ', 'ϥ', 'ⲥ', 'ⲛ', 'ⲧⲛ', 'ⲩ']),

    % Verb (infinitive)
    nth1(VIdx, Words, word(Verb, 'VERB', _)),

    % Order: AUX < PRON < VERB (ⲁ-ϥ-ⲃⲱⲕ)
    AIdx < PIdx,
    PIdx < VIdx.

% Pattern 10: Imperative (Layton Lesson 11, §91-97)
% Example: ⲁⲣⲓⲕⲃⲱⲕ (arik-bwk = "Go!" to you masc.sing)
% Structure: Imperative marker (ⲁⲣⲓⲕ) + Infinitive (ⲃⲱⲕ)
%
% Dependency:
%   ⲃⲱⲕ (VERB, root)
%   └── ⲁⲣⲓⲕ (AUX, aux) - imperative marker
%
dependency_pattern(imperative,
    Words,
    [dep(ImpMarker, 'AUX', IIdx, Verb, VIdx, aux)]) :-
    % Imperative marker
    nth1(IIdx, Words, word(ImpMarker, 'AUX', _)),
    member(ImpMarker, ['ⲁⲣⲓⲕ', 'ⲁⲣⲓⲧⲉ', 'ⲁⲣⲓⲧⲛ', 'ⲙⲡⲣⲕ', 'ⲙⲡⲣⲧⲉ', 'ⲙⲡⲣⲧⲛ']),
    % ⲁⲣⲓ- (affirmative), ⲙⲡⲣ- (negative)

    % Verb (infinitive)
    nth1(VIdx, Words, word(Verb, 'VERB', _)),

    % Order: IMP < VERB
    IIdx < VIdx.

% Pattern 11: Causative (Layton Lesson 13, §111-114) - DISABLED
%
% TODO: Requires proper xcomp analysis per UD guidelines (COPTIC_UD_ALIGNMENT.md:239-256)
%
% Example: ⲧⲣⲉϥⲙⲟⲩ (tre-f-mu = "cause him to die" = "kill him")
% Structure: Causative marker (ⲧⲣⲉ) + Pronoun (ϥ) + Infinitive (ⲙⲟⲩ)
%
% ISSUE: UD guidelines show causative should use xcomp, not aux:
%   Correct structure:
%   ⲧⲣⲉ (VERB, root or xcomp)
%   ├── ϥ (nsubj, causee - needs clarification)
%   └── ⲙⲟⲩ (xcomp, caused action)
%
% Current implementation below uses aux (incorrect). Requires full analysis of
% Layton §111-114 to determine correct attachment points and whether ⲧⲣⲉ is root/xcomp.
%
% Disabled until proper implementation:
%
% dependency_pattern(causative,
%     Words,
%     [dep(CausMarker, 'AUX', CIdx, Verb, VIdx, aux),
%      dep(Pron, 'PRON', PIdx, Verb, VIdx, nsubj)]) :-
%     nth1(CIdx, Words, word(CausMarker, 'AUX', _)),
%     atom_concat('ⲧⲣⲉ', _, CausMarker),
%     nth1(PIdx, Words, word(Pron, 'PRON', _)),
%     nth1(VIdx, Words, word(Verb, 'VERB', _)),
%     CIdx < PIdx,
%     PIdx < VIdx.
%
% dependency_pattern(causative_fused,
%     Words,
%     [dep(CausPron, 'AUX', CPIdx, Verb, VIdx, aux)]) :-
%     nth1(CPIdx, Words, word(CausPron, 'AUX', _)),
%     member(CausPron, ['ⲧⲣⲁ', 'ⲧⲣⲉⲕ', 'ⲧⲣⲉϥ', 'ⲧⲣⲉⲥ', 'ⲧⲣⲉⲛ', 'ⲧⲣⲉⲧⲛ', 'ⲧⲣⲉⲩ']),
%     nth1(VIdx, Words, word(Verb, 'VERB', _)),
%     CPIdx < VIdx.

% Pattern 12: Circumstantial (Layton Lesson 15, §120)
% Example: ⲉϥⲥⲱⲧⲙ (e-f-swtm = "when/while he hears")
% Structure: Circumstantial converter (ⲉ) + Pronoun (ϥ) + Infinitive (ⲥⲱⲧⲙ)
%
% Dependency:
%   ⲥⲱⲧⲙ (VERB, root of subordinate clause)
%   ├── ⲉ (SCONJ, mark) - circumstantial converter
%   └── ϥ (PRON, nsubj)
%
dependency_pattern(circumstantial,
    Words,
    [dep(Conv, 'SCONJ', CIdx, Verb, VIdx, mark),
     dep(Pron, 'PRON', PIdx, Verb, VIdx, nsubj)]) :-
    % Circumstantial converter
    nth1(CIdx, Words, word(Conv, 'SCONJ', _)),
    member(Conv, ['ⲉ', 'ⲉⲣⲉ']),  % ⲉ- with pronoun, ⲉⲣⲉ- with noun

    % Pronominal subject
    nth1(PIdx, Words, word(Pron, 'PRON', _)),

    % Verb
    nth1(VIdx, Words, word(Verb, 'VERB', _)),

    % Order: CONV < PRON < VERB
    CIdx < PIdx,
    PIdx < VIdx.

% Pattern 13: Second Tense / Focalizing (Layton Lesson 18, §143-145)
% Example: ⲛⲧⲁϥⲉⲓ (nta-f-ei = "it was that he came")
% Structure: Focalizing marker (ⲛⲧⲁ) + Pronoun (ϥ) + Infinitive (ⲉⲓ)
%
% Dependency:
%   ⲉⲓ (VERB, root)
%   ├── ⲛⲧⲁ (AUX, aux) - focalizing marker
%   └── ϥ (PRON, nsubj)
%
dependency_pattern(focalizing,
    Words,
    [dep(Foc, 'AUX', FIdx, Verb, VIdx, aux),
     dep(Pron, 'PRON', PIdx, Verb, VIdx, nsubj)]) :-
    % Focalizing marker
    nth1(FIdx, Words, word(Foc, 'AUX', _)),
    member(Foc, ['ⲛⲧⲁ', 'ⲛⲧⲉ', 'ⲉⲧ']),  % Second tense markers

    % Pronominal subject
    nth1(PIdx, Words, word(Pron, 'PRON', _)),

    % Verb
    nth1(VIdx, Words, word(Verb, 'VERB', _)),

    % Order: FOC < PRON < VERB
    FIdx < PIdx,
    PIdx < VIdx.

% Pattern 14: Prepositional Object (ⲙⲙⲟϥ = "him" accusative)
% Example: ⲁϥⲥⲱⲧⲙ ⲙⲙⲟϥ (a-f-swtm mmo-f = "he heard him")
% Structure: Prep (ⲙⲙⲟ) + Pronoun (ϥ)
%
% Dependency:
%   ϥ (PRON, obj to verb)
%   └── ⲙⲙⲟ (ADP, case)
%
dependency_pattern(prepositional_object,
    Words,
    [dep(Prep, 'ADP', PrepIdx, Pron, PIdx, case),
     dep(Pron, 'PRON', PIdx, Verb, VIdx, obj)]) :-
    % Verb
    nth1(VIdx, Words, word(Verb, 'VERB', _)),

    % Preposition (object marker)
    nth1(PrepIdx, Words, word(Prep, 'ADP', _)),
    member(Prep, ['ⲙⲙⲟ', 'ⲛⲁ', 'ⲉⲣⲟ', 'ϩⲁⲣⲟ']),

    % Pronominal object
    nth1(PIdx, Words, word(Pron, 'PRON', _)),

    % Order: VERB < PREP < PRON
    VIdx < PrepIdx,
    PrepIdx < PIdx.

%******************************************************************************
% CONSTRAINT CHECKING
%******************************************************************************

% Check if verb is transitive (requires object)
is_transitive(Verb) :-
    coptic_verb(Verb, Features),
    member(transitive, Features), !.
is_transitive(_).  % Default: assume transitive if unknown

% Check if verb is intransitive (no object)
is_intransitive(Verb) :-
    coptic_verb(Verb, Features),
    member(intransitive, Features), !.
is_intransitive(_).  % Default: allow intransitive

% Copula-predicate agreement
copula_agrees_with_predicate(Cop, Pred) :-
    coptic_noun(Pred, Gender, Number), !,
    copula_form(Cop, Gender, Number).
copula_agrees_with_predicate(_, _).  % Allow if not in lexicon

copula_form('ⲡⲉ', masc, sing).
copula_form('ⲧⲉ', fem, sing).
copula_form('ⲛⲉ', _, plur).
copula_form('ⲛⲉ', masc, plur).
copula_form('ⲛⲉ', fem, plur).

% Determiner-noun gender agreement
determiner_gender_agrees(Det, Noun) :-
    coptic_noun(Noun, Gender, Number), !,
    determiner_form(Det, Gender, Number).
determiner_gender_agrees(_, _).  % Allow if not in lexicon

determiner_form('ⲡ', masc, sing).
determiner_form('ⲧ', fem, sing).
determiner_form('ⲛ', _, plur).
determiner_form('ⲟⲩ', _, _).  % Indefinite: any gender/number

% Adjective-noun agreement
adjective_agrees(Adj, Noun) :-
    coptic_noun(Noun, Gender, Number),
    coptic_adjective(Adj, Gender, Number), !.
adjective_agrees(_, _).  % Allow if not in lexicon

%******************************************************************************
% VALIDATION AND ERROR DETECTION
%******************************************************************************

% validate_dependency(+Token, +Head, +Relation, +Words)
% Check if a proposed dependency is valid according to Coptic grammar
validate_dependency(Token, Head, Relation, Words) :-
    % Find positions
    nth1(TokenIdx, Words, word(Token, TokenPOS, _)),
    nth1(HeadIdx, Words, word(Head, HeadPOS, _)),

    % Check if relation is valid for this POS pair
    valid_relation(TokenPOS, HeadPOS, Relation),

    % Check linguistic constraints
    check_constraints(Token, TokenPOS, TokenIdx, Head, HeadPOS, HeadIdx, Relation, Words).

% Valid dependency relations (simplified from UD)
valid_relation('NOUN', 'VERB', nsubj).
valid_relation('PRON', 'VERB', nsubj).
valid_relation('PROPN', 'VERB', nsubj).
valid_relation('NOUN', 'VERB', obj).
valid_relation('PRON', 'VERB', obj).
valid_relation('NOUN', 'NOUN', nmod).
valid_relation('ADJ', 'NOUN', amod).
valid_relation('DET', 'NOUN', det).
valid_relation('ADP', 'NOUN', case).
valid_relation('ADP', 'PRON', case).
valid_relation('AUX', 'NOUN', cop).
valid_relation('AUX', 'ADJ', cop).
valid_relation('CCONJ', 'NOUN', cc).
valid_relation('CCONJ', 'VERB', cc).
valid_relation(_, _, root).  % Root can be anything

% Constraint checking
check_constraints(_Token, _TokenPOS, TokenIdx, _Head, HeadPOS, HeadIdx, Relation, _Words) :-
    % Word order constraints
    (   Relation = nsubj,
        member(HeadPOS, ['VERB', 'AUX'])
    ->  % In VSO, subject follows verb
        TokenIdx > HeadIdx
    ;   true
    ),

    (   Relation = obj,
        HeadPOS = 'VERB'
    ->  % Object follows subject in VSO
        TokenIdx > HeadIdx
    ;   true
    ),

    (   Relation = det
    ->  % Determiner precedes noun
        TokenIdx < HeadIdx
    ;   true
    ),

    (   Relation = amod
    ->  % Adjective typically follows noun in Coptic
        TokenIdx > HeadIdx
    ;   true
    ).

%******************************************************************************
% PARSING WITH DEPENDENCY RULES
%******************************************************************************

% suggest_parse(+Words, +POSTags, -Dependencies)
% Use dependency rules to suggest a parse
suggest_parse(Words, POSTags, Dependencies) :-
    % Build word structures
    length(Words, N),
    build_word_list(Words, POSTags, 1, N, WordList),

    % Try to match patterns
    findall(Deps, dependency_pattern(_, WordList, Deps), AllDeps),

    % Combine non-overlapping dependencies
    flatten(AllDeps, FlatDeps),
    sort(FlatDeps, Dependencies).

build_word_list([], [], _, _, []).
build_word_list([W|Ws], [P|Ps], Idx, N, [word(W, P, Idx)|Rest]) :-
    NextIdx is Idx + 1,
    build_word_list(Ws, Ps, NextIdx, N, Rest).

% apply_dependency_rules(+Tokens, +POSTags, -ParseTree)
% Full parsing using dependency rules
apply_dependency_rules(Tokens, POSTags, ParseTree) :-
    suggest_parse(Tokens, POSTags, Dependencies),

    % Find root
    (   select(dep(Root, RootPOS, RootIdx, _, 0, root), Dependencies, OtherDeps)
    ->  true
    ;   % No root found - pick first verb or noun
        nth1(RootIdx, POSTags, RootPOS),
        member(RootPOS, ['VERB', 'NOUN', 'AUX']),
        nth1(RootIdx, Tokens, Root),
        OtherDeps = Dependencies
    ),

    ParseTree = dep_tree{
        root: Root,
        root_pos: RootPOS,
        root_index: RootIdx,
        dependencies: OtherDeps,
        parser: 'Dependency Rules'
    }.

%******************************************************************************
% COMPARISON: DCG vs DEPENDENCY
%******************************************************************************

% EXAMPLE: How DETECT5.PRO might have encoded a rule
%
% DCG Style (old):
%   sentence --> verb_phrase.
%   verb_phrase --> verb(V, trans), noun_phrase(Subj), noun_phrase(Obj),
%                   {vso_order(V, Subj, Obj)}.
%   noun_phrase --> determiner(D), noun(N), {gender_agrees(D, N)}.
%
% Dependency Style (new):
%   dependency_pattern(vso,
%       [verb(V, VIdx), noun(S, SIdx), noun(O, OIdx)],
%       [dep(S, SIdx, V, VIdx, nsubj),
%        dep(O, OIdx, V, VIdx, obj)]) :-
%       VIdx < SIdx, SIdx < OIdx.
%
% KEY DIFFERENCES:
% 1. DCG builds hierarchical structure (VP contains NPs)
% 2. Dependency expresses direct relations (verb governs subject)
% 3. Dependency is more flexible for free word order
% 4. Dependency better matches modern neural parser output

%******************************************************************************
% END OF MODULE
%******************************************************************************
