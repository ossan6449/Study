create schema signate;



create table train (
	datetid timestamp,
	y int,
	week char,
	soldout boolean,
	name varchar,
	kcal int,
	remarks varchar,
	event varchar,
	payday boolean,
	weather varchar,
	precipitation float,
	temperature float
);


create table test (
	datetid timestamp,
	y int,
	week char,
	soldout boolean,
	name varchar,
	kcal int,
	remarks varchar,
	event varchar,
	payday boolean,
	weather varchar,
	precipitation float,
	temperature float
);



create table wk_train (
	datetid text,
	y text,
	week text,
	soldout text,
	name text,
	kcal text,
	remarks text,
	event text,
	payday text,
	weather text,
	precipitation text,
	temperature text
);


create table wk_test (
	datetid text,
	y text,
	week text,
	soldout text,
	name text,
	kcal text,
	remarks text,
	event text,
	payday text,
	weather text,
	precipitation text,
	temperature text
);



















SELECT * FROM column_test;










DROP TABLE column_test;

CREATE TABLE column_test (	
	col001 text primary key,
	col002 text,
	col003 text,
	col004 text,
	col005 text,
	col006 text,
	col007 text,
	col008 text,
	col009 text,
	col010 text,
	col011 text,
	col012 text,
	col013 text,
	col014 text,
	col015 text,
	col016 text,
	col017 text,
	col018 text,
	col019 text,
	col020 text,
	col021 text,
	col022 text,
	col023 text,
	col024 text,
	col025 text,
	col026 text,
	col027 text,
	col028 text,
	col029 text,
	col030 text,
	col031 text,
	col032 text,
	col033 text,
	col034 text,
	col035 text,
	col036 text,
	col037 text,
	col038 text,
	col039 text,
	col040 text,
	col041 text,
	col042 text,
	col043 text,
	col044 text,
	col045 text,
	col046 text,
	col047 text,
	col048 text,
	col049 text,
	col050 text,
	col051 text,
	col052 text,
	col053 text,
	col054 text,
	col055 text,
	col056 text,
	col057 text,
	col058 text,
	col059 text,
	col060 text,
	col061 text,
	col062 text,
	col063 text,
	col064 text,
	col065 text,
	col066 text,
	col067 text,
	col068 text,
	col069 text,
	col070 text,
	col071 text,
	col072 text,
	col073 text,
	col074 text,
	col075 text,
	col076 text,
	col077 text,
	col078 text,
	col079 text,
	col080 text,
	col081 text,
	col082 text,
	col083 text,
	col084 text,
	col085 text,
	col086 text,
	col087 text,
	col088 text,
	col089 text,
	col090 text,
	col091 text,
	col092 text,
	col093 text,
	col094 text,
	col095 text,
	col096 text,
	col097 text,
	col098 text,
	col099 text,
	col100 text,
	col101 text,
	col102 text,
	col103 text,
	col104 text,
	col105 text,
	col106 text,
	col107 text,
	col108 text,
	col109 text,
	col110 text,
	col111 text,
	col112 text,
	col113 text,
	col114 text,
	col115 text,
	col116 text,
	col117 text,
	col118 text,
	col119 text,
	col120 text,
	col121 text,
	col122 text,
	col123 text,
	col124 text,
	col125 text,
	col126 text,
	col127 text,
	col128 text,
	col129 text,
	col130 text,
	col131 text,
	col132 text,
	col133 text,
	col134 text,
	col135 text,
	col136 text,
	col137 text,
	col138 text,
	col139 text,
	col140 text,
	col141 text,
	col142 text,
	col143 text,
	col144 text,
	col145 text,
	col146 text,
	col147 text,
	col148 text,
	col149 text,
	col150 text,
	col151 text,
	col152 text,
	col153 text,
	col154 text,
	col155 text,
	col156 text,
	col157 text,
	col158 text,
	col159 text,
	col160 text,
	col161 text,
	col162 text,
	col163 text,
	col164 text,
	col165 text,
	col166 text,
	col167 text,
	col168 text,
	col169 text,
	col170 text,
	col171 text,
	col172 text,
	col173 text,
	col174 text,
	col175 text,
	col176 text,
	col177 text,
	col178 text,
	col179 text,
	col180 text,
	col181 text,
	col182 text,
	col183 text,
	col184 text,
	col185 text,
	col186 text,
	col187 text,
	col188 text,
	col189 text,
	col190 text,
	col191 text,
	col192 text,
	col193 text,
	col194 text,
	col195 text,
	col196 text,
	col197 text,
	col198 text,
	col199 text,
	col200 text,
	col201 text,
	col202 text,
	col203 text,
	col204 text,
	col205 text,
	col206 text,
	col207 text,
	col208 text,
	col209 text,
	col210 text,
	col211 text,
	col212 text,
	col213 text,
	col214 text,
	col215 text,
	col216 text,
	col217 text,
	col218 text,
	col219 text,
	col220 text,
	col221 text,
	col222 text,
	col223 text,
	col224 text,
	col225 text,
	col226 text,
	col227 text,
	col228 text,
	col229 text,
	col230 text,
	col231 text,
	col232 text,
	col233 text,
	col234 text,
	col235 text,
	col236 text,
	col237 text,
	col238 text,
	col239 text,
	col240 text,
	col241 text,
	col242 text,
	col243 text,
	col244 text,
	col245 text,
	col246 text,
	col247 text,
	col248 text,
	col249 text,
	col250 text,
	col251 text,
	col252 text,
	col253 text,
	col254 text,
	col255 text,
	col256 text,
	col257 text,
	col258 text,
	col259 text,
	col260 text,
	col261 text,
	col262 text,
	col263 text,
	col264 text,
	col265 text,
	col266 text,
	col267 text,
	col268 text,
	col269 text,
	col270 text,
	col271 text,
	col272 text,
	col273 text,
	col274 text,
	col275 text,
	col276 text,
	col277 text,
	col278 text,
	col279 text,
	col280 text,
	col281 text,
	col282 text,
	col283 text,
	col284 text,
	col285 text,
	col286 text,
	col287 text,
	col288 text,
	col289 text,
	col290 text,
	col291 text,
	col292 text,
	col293 text,
	col294 text,
	col295 text,
	col296 text,
	col297 text,
	col298 text,
	col299 text,
	col300 text,
	col301 text,
	col302 text,
	col303 text,
	col304 text,
	col305 text,
	col306 text,
	col307 text,
	col308 text,
	col309 text,
	col310 text,
	col311 text,
	col312 text,
	col313 text,
	col314 text,
	col315 text,
	col316 text,
	col317 text,
	col318 text,
	col319 text,
	col320 text,
	col321 text,
	col322 text,
	col323 text,
	col324 text,
	col325 text,
	col326 text,
	col327 text,
	col328 text,
	col329 text,
	col330 text,
	col331 text,
	col332 text,
	col333 text,
	col334 text,
	col335 text,
	col336 text,
	col337 text,
	col338 text,
	col339 text,
	col340 text,
	col341 text,
	col342 text,
	col343 text,
	col344 text,
	col345 text,
	col346 text,
	col347 text,
	col348 text,
	col349 text,
	col350 text,
	col351 text,
	col352 text,
	col353 text,
	col354 text,
	col355 text,
	col356 text,
	col357 text,
	col358 text,
	col359 text,
	col360 text,
	col361 text,
	col362 text,
	col363 text,
	col364 text,
	col365 text,
	col366 text,
	col367 text,
	col368 text,
	col369 text,
	col370 text,
	col371 text,
	col372 text,
	col373 text,
	col374 text,
	col375 text,
	col376 text,
	col377 text,
	col378 text,
	col379 text,
	col380 text,
	col381 text,
	col382 text,
	col383 text,
	col384 text,
	col385 text,
	col386 text,
	col387 text,
	col388 text,
	col389 text,
	col390 text,
	col391 text,
	col392 text,
	col393 text,
	col394 text,
	col395 text,
	col396 text,
	col397 text,
	col398 text,
	col399 text,
	col400 text,
	col401 text,
	col402 text,
	col403 text,
	col404 text,
	col405 text,
	col406 text,
	col407 text,
	col408 text,
	col409 text,
	col410 text,
	col411 text,
	col412 text,
	col413 text,
	col414 text,
	col415 text,
	col416 text,
	col417 text,
	col418 text,
	col419 text,
	col420 text,
	col421 text,
	col422 text,
	col423 text,
	col424 text,
	col425 text,
	col426 text,
	col427 text,
	col428 text,
	col429 text,
	col430 text,
	col431 text,
	col432 text,
	col433 text,
	col434 text,
	col435 text,
	col436 text,
	col437 text,
	col438 text,
	col439 text,
	col440 text,
	col441 text,
	col442 text,
	col443 text,
	col444 text,
	col445 text,
	col446 text,
	col447 text,
	col448 text,
	col449 text,
	col450 text,
	col451 text,
	col452 text,
	col453 text,
	col454 text,
	col455 text,
	col456 text,
	col457 text,
	col458 text,
	col459 text,
	col460 text,
	col461 text,
	col462 text,
	col463 text,
	col464 text,
	col465 text,
	col466 text,
	col467 text,
	col468 text,
	col469 text,
	col470 text,
	col471 text,
	col472 text,
	col473 text,
	col474 text,
	col475 text,
	col476 text,
	col477 text,
	col478 text,
	col479 text,
	col480 text,
	col481 text,
	col482 text,
	col483 text,
	col484 text,
	col485 text,
	col486 text,
	col487 text,
	col488 text,
	col489 text,
	col490 text,
	col491 text,
	col492 text,
	col493 text,
	col494 text,
	col495 text,
	col496 text,
	col497 text,
	col498 text,
	col499 text,
	col500 text,
	col501 text,
	col502 text,
	col503 text,
	col504 text,
	col505 text,
	col506 text,
	col507 text,
	col508 text,
	col509 text,
	col510 text,
	col511 text,
	col512 text,
	col513 text,
	col514 text,
	col515 text,
	col516 text,
	col517 text,
	col518 text,
	col519 text,
	col520 text,
	col521 text,
	col522 text,
	col523 text,
	col524 text,
	col525 text,
	col526 text,
	col527 text,
	col528 text,
	col529 text,
	col530 text,
	col531 text,
	col532 text,
	col533 text,
	col534 text,
	col535 text,
	col536 text,
	col537 text,
	col538 text,
	col539 text,
	col540 text,
	col541 text,
	col542 text,
	col543 text,
	col544 text,
	col545 text,
	col546 text,
	col547 text,
	col548 text,
	col549 text,
	col550 text,
	col551 text,
	col552 text,
	col553 text,
	col554 text,
	col555 text,
	col556 text,
	col557 text,
	col558 text,
	col559 text,
	col560 text,
	col561 text,
	col562 text,
	col563 text,
	col564 text,
	col565 text,
	col566 text,
	col567 text,
	col568 text,
	col569 text,
	col570 text,
	col571 text,
	col572 text,
	col573 text,
	col574 text,
	col575 text,
	col576 text,
	col577 text,
	col578 text,
	col579 text,
	col580 text,
	col581 text,
	col582 text,
	col583 text,
	col584 text,
	col585 text,
	col586 text,
	col587 text,
	col588 text,
	col589 text,
	col590 text,
	col591 text,
	col592 text,
	col593 text,
	col594 text,
	col595 text,
	col596 text,
	col597 text,
	col598 text,
	col599 text,
	col600 text,
	col601 text,
	col602 text,
	col603 text,
	col604 text,
	col605 text,
	col606 text,
	col607 text,
	col608 text,
	col609 text,
	col610 text,
	col611 text,
	col612 text,
	col613 text,
	col614 text,
	col615 text,
	col616 text,
	col617 text,
	col618 text,
	col619 text,
	col620 text,
	col621 text,
	col622 text,
	col623 text,
	col624 text,
	col625 text,
	col626 text,
	col627 text,
	col628 text,
	col629 text,
	col630 text,
	col631 text,
	col632 text,
	col633 text,
	col634 text,
	col635 text,
	col636 text,
	col637 text,
	col638 text,
	col639 text,
	col640 text,
	col641 text,
	col642 text,
	col643 text,
	col644 text,
	col645 text,
	col646 text,
	col647 text,
	col648 text,
	col649 text,
	col650 text,
	col651 text,
	col652 text,
	col653 text,
	col654 text,
	col655 text,
	col656 text,
	col657 text,
	col658 text,
	col659 text,
	col660 text,
	col661 text,
	col662 text,
	col663 text,
	col664 text,
	col665 text,
	col666 text,
	col667 text,
	col668 text,
	col669 text,
	col670 text,
	col671 text,
	col672 text,
	col673 text,
	col674 text,
	col675 text,
	col676 text,
	col677 text,
	col678 text,
	col679 text,
	col680 text,
	col681 text,
	col682 text,
	col683 text,
	col684 text,
	col685 text,
	col686 text,
	col687 text,
	col688 text,
	col689 text,
	col690 text,
	col691 text,
	col692 text,
	col693 text,
	col694 text,
	col695 text,
	col696 text,
	col697 text,
	col698 text,
	col699 text,
	col700 text,
	col701 text,
	col702 text,
	col703 text,
	col704 text,
	col705 text,
	col706 text,
	col707 text,
	col708 text,
	col709 text,
	col710 text,
	col711 text,
	col712 text,
	col713 text,
	col714 text,
	col715 text,
	col716 text,
	col717 text,
	col718 text,
	col719 text,
	col720 text,
	col721 text,
	col722 text,
	col723 text,
	col724 text,
	col725 text,
	col726 text,
	col727 text,
	col728 text,
	col729 text,
	col730 text,
	col731 text,
	col732 text,
	col733 text,
	col734 text,
	col735 text,
	col736 text,
	col737 text,
	col738 text,
	col739 text,
	col740 text,
	col741 text,
	col742 text,
	col743 text,
	col744 text,
	col745 text,
	col746 text,
	col747 text,
	col748 text,
	col749 text,
	col750 text,
	col751 text,
	col752 text,
	col753 text,
	col754 text,
	col755 text,
	col756 text,
	col757 text,
	col758 text,
	col759 text,
	col760 text,
	col761 text,
	col762 text,
	col763 text,
	col764 text,
	col765 text,
	col766 text,
	col767 text,
	col768 text,
	col769 text,
	col770 text,
	col771 text,
	col772 text,
	col773 text,
	col774 text,
	col775 text,
	col776 text,
	col777 text,
	col778 text,
	col779 text,
	col780 text,
	col781 text,
	col782 text,
	col783 text,
	col784 text,
	col785 text,
	col786 text,
	col787 text,
	col788 text,
	col789 text,
	col790 text,
	col791 text,
	col792 text,
	col793 text,
	col794 text,
	col795 text,
	col796 text,
	col797 text,
	col798 text,
	col799 text,
	col800 text,
	col801 text,
	col802 text,
	col803 text,
	col804 text,
	col805 text,
	col806 text,
	col807 text,
	col808 text,
	col809 text,
	col810 text,
	col811 text,
	col812 text,
	col813 text,
	col814 text,
	col815 text,
	col816 text,
	col817 text,
	col818 text,
	col819 text,
	col820 text,
	col821 text,
	col822 text,
	col823 text,
	col824 text,
	col825 text,
	col826 text,
	col827 text,
	col828 text,
	col829 text,
	col830 text,
	col831 text,
	col832 text,
	col833 text,
	col834 text,
	col835 text,
	col836 text,
	col837 text,
	col838 text,
	col839 text,
	col840 text,
	col841 text,
	col842 text,
	col843 text,
	col844 text,
	col845 text,
	col846 text,
	col847 text,
	col848 text,
	col849 text,
	col850 text,
	col851 text,
	col852 text,
	col853 text,
	col854 text,
	col855 text,
	col856 text,
	col857 text,
	col858 text,
	col859 text,
	col860 text,
	col861 text,
	col862 text,
	col863 text,
	col864 text,
	col865 text,
	col866 text,
	col867 text,
	col868 text,
	col869 text,
	col870 text,
	col871 text,
	col872 text,
	col873 text,
	col874 text,
	col875 text,
	col876 text,
	col877 text,
	col878 text,
	col879 text,
	col880 text,
	col881 text,
	col882 text,
	col883 text,
	col884 text,
	col885 text,
	col886 text,
	col887 text,
	col888 text,
	col889 text,
	col890 text,
	col891 text,
	col892 text,
	col893 text,
	col894 text,
	col895 text,
	col896 text,
	col897 text,
	col898 text,
	col899 text,
	col900 text,
	col901 text,
	col902 text,
	col903 text,
	col904 text,
	col905 text,
	col906 text,
	col907 text,
	col908 text,
	col909 text,
	col910 text,
	col911 text,
	col912 text,
	col913 text,
	col914 text,
	col915 text,
	col916 text,
	col917 text,
	col918 text,
	col919 text,
	col920 text,
	col921 text,
	col922 text,
	col923 text,
	col924 text,
	col925 text,
	col926 text,
	col927 text,
	col928 text,
	col929 text,
	col930 text,
	col931 text,
	col932 text,
	col933 text,
	col934 text,
	col935 text,
	col936 text,
	col937 text,
	col938 text,
	col939 text,
	col940 text,
	col941 text,
	col942 text,
	col943 text,
	col944 text,
	col945 text,
	col946 text,
	col947 text,
	col948 text,
	col949 text,
	col950 text,
	col951 text,
	col952 text,
	col953 text,
	col954 text,
	col955 text,
	col956 text,
	col957 text,
	col958 text,
	col959 text,
	col960 text,
	col961 text,
	col962 text,
	col963 text,
	col964 text,
	col965 text,
	col966 text,
	col967 text,
	col968 text,
	col969 text,
	col970 text,
	col971 text,
	col972 text,
	col973 text,
	col974 text,
	col975 text,
	col976 text,
	col977 text,
	col978 text,
	col979 text,
	col980 text,
	col981 text,
	col982 text,
	col983 text,
	col984 text,
	col985 text,
	col986 text,
	col987 text,
	col988 text,
	col989 text,
	col990 text,
	col991 text,
	col992 text,
	col993 text,
	col994 text,
	col995 text,
	col996 text,
	col997 text,
	col998 text,
	col999 text,
	col1000 text,
	col1001 text
);	

