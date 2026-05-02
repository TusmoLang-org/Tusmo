# semantic_errors.py

class SemanticError(Exception):
    def __init__(self, message, filename="unknown", line="unknown"):
        self.message = message
        self.filename = filename
        self.line = line
        super().__init__(self.message)

    def __str__(self):
        return (
            f"\033[91m\033[1m[!] KHALAD:\033[0m {self.message}\n"
            f"\033[90m" + ("-" * 45) + "\033[0m\n"
            f"\033[94mFaylka:\033[0m   {self.filename}\n"
            f"\033[94mSaddarka:\033[0m {self.line}\n"
        )

# --- Helper functions to generate "Canaan" (Scolding) error messages ---

def ERR_UNRECOGNIZED_NAMED_ARG(arg_name, context):
    return f"""Magac halbeeg ee '{arg_name}' ma ahan mid la'aqoonsan yahay. 
    
        \033[1;31m {context}({arg_name}) \033[1;35m // Halkee ka keentay '{arg_name}'? Ma adigaa iska dhisay?
        \033[1;32m // Hubi magacyada halbeegyada ee hawsha '{context}'."""

def ERR_DUPLICATE_NAMED_ARG(arg_name, context):
    return f"""Halbeegga '{arg_name}' waxaa la siiyay in kabadan hal jeer!
                                         
        \033[1;31m {context}({arg_name} = ..., {arg_name} = ...) \033[1;35m 
        // Maxaa sababay in halbeegga '{arg_name}' aad u yeerto in ka badan hal jeer? 
        // Ma waxaad moodday inuu kaaga jawaabayo haddii aad laba jeer u yeerto?"""

def ERR_POSITIONAL_AFTER_NAMED(context):
    return f"""Naxwahaaga sax! Halbeegyada wata magac (named args) waa inay had iyo jeer u dambeeyaan.
    
        \033[1;31m {context}(magac = "Tusmo", 2.1) \033[1;35m // Sidani waa khalad!
        \033[1;32m {context}(2.1, magac = "Tusmo") \033[1;35m // Sidani waa naxwe sax ah."""

def ERR_MISSING_ARG(param_name, context, khalad_list, sax_list):
    return f"""Halbeegga muhiimka ah ee '{param_name}' ayaa maqan markaad u yeeraysay '{context}'.
    
        \033[1;31m {context}({khalad_list}) \033[1;35m // Sidee ku rabtaa in '{context}' ay shaqayso adigoo aan siin '{param_name}'?
        \033[1;32m {context}({sax_list}) \033[1;35m // Buuxi dhammaan halbeegyada lagama maarmaanka ah."""

def ERR_KAN_OUTSIDE_KOOX():
    return f"""Isticmaalka 'kan' (this) halkan ma bannaana! Waxaa loo isticmaali karaa oo kaliya gudaha koox (class).
    
        \033[1;31m hawl magac() {{ kan.x = 10; }} \033[1;35m // 'kan' ma yaqaanno cidda uu yahay haddii uusan koox ku jirin!
        \033[1;32m koox Qof {{ hawl magac() {{ kan.x = 10; }} }} \033[1;35m // Halkan waa booska saxda ah."""

def ERR_UNDEFINED_VARIABLE(name):
    return f"""Keydiyaha '{name}' lama helin! 
    
        \033[1;31m qor({name}) \033[1;35m // '{name}' lama dhisin wali. Ma waxaad moodday inuu iska dhalanayo?
        \033[1;32m keyd:tiro {name} = 10; qor({name}) \033[1;35m // Horta dhis, ka dibna u yeer!"""

def ERR_TYPE_MISMATCH(expected, actual):
    return f"""Noocyada xogta iskuma mid ahan (Type Mismatch)!
    
        \033[1;31m keyd:{expected} x = {actual}_value; \033[1;35m // Sidee '{actual}' ugu dhex riday '{expected}'? 
        \033[1;35m // Ma maroodi baad rabtaa inaad dhal yar ku dhex rido?
        \033[1;32m keyd:{expected} x = {expected}_value; \033[1;35m // Isku dhig wax isku nooc ah."""

def ERR_ASSIGNMENT_TYPE_MISMATCH_SIMPLE(expected_type, actual_type):
    return f"""Noocyada xogta iskuma mid ahan (Type Mismatch)!
    
        \033[1;31m keyd:{expected_type} x = qiyam_kan; \033[1;35m // Qiimaha '{actual_type}' kuma fadhiiya '{expected_type}'
        \033[1;32m keyd:{expected_type} x = {expected_type}_qiime; \033[1;35m // Isticmaal qiime isku nooc ah."""

def ERR_INVALID_LHS_ASSIGNMENT():
    return f"""Xisaabtaada sax! Qiime lama gelin karo dhinaca bidix ee calaamadda '='.
    
        \033[1;31m 10 = x; \033[1;35m // Sidee '10' qiime loogu ridi karaa? '10' waa '10' waligeed!
        \033[1;32m x = 10; \033[1;35m // Qiimaha had iyo jeer midigta ka keen."""

def ERR_IDENTIFIER_NOT_FOUND(name):
    return f"""Magaca '{name}' lama yaqaan.
    
        \033[1;31m {name}(); \033[1;35m // '{name}' ma jirto. Ma riyo baad ku aragtay magacan?
        \033[1;32m // Hubi inaad si sax ah u qortay ama aad 'keen' ku soo dartay module-ka."""

def ERR_FUNCTION_NOT_FOUND(name):
    return f"""Hawsha '{name}' lama helin ama maahan hawl run ah.
    
        \033[1;31m {name}(); \033[1;35m // Ma jiro qof kuu dhisay hawl magacan leh.
        \033[1;32m hawl {name}() {{ ... }} \033[1;35m // Marka hore qeex hawsha aad u baahan tahay."""

def ERR_NOT_AN_ARRAY(identifier, actual_type):
    return f"""'{identifier}' maaha tix (array) ee waa '{actual_type}'!
    
        \033[1;31m {identifier}[0] \033[1;35m // '{actual_type}' ma leh boosas aad wax ka akhrido.
        \033[1;32m keyd:tix:tiro t = [1, 2]; t[0] \033[1;35m // Tixaha kaliya ayaa leh [] boosas."""

def ERR_MEMBER_NOT_FOUND(class_name, member_name):
    return f"""Kooxda '{class_name}' malaha xubin la yiraahdo '{member_name}'.
    
        \033[1;31m {class_name}.{member_name}; \033[1;35m // Xubintan kuma jirto kooxda. 
        \033[1;35m // Ma waxaad rabtaa inaad kooxda ku dhex dhumisid wax aan jirin?
        \033[1;32m // Hubi liiska xubnaha (keyd/hawl) ee ku dhex jira '{class_name}'."""




def ERR_TOO_MANY_ARGS(context):
    return f"""Wicitaanka '{context}' wuxuu helay halbeegyo ka badan intii loo qoondeeyay!
    
        \033[1;31m {context}(1, 2, 3, 4, 5...) \033[1;35m // Maxaa halbeegyada intan le'eg isugu soo dhuftay?
        \033[1;32m // Hubi tirada saxda ah ee hawsha '{context}' ay u baahan tahay."""

def ERR_RETURN_OUTSIDE_FUNCTION():
    return f"""'soo_celi' (return) ma iska dhex ooyi karo meel walba!
    
        \033[1;31m soo_celi 10; \033[1;35m // Meeshaad u celinaysaa qiimaha adigoon hawl ku jirin?
        \033[1;32m hawl h() {{ soo_celi 10; }} \033[1;35m // 'soo_celi' wuxuu ka shaqeeyaa gudaha hawlaha."""

def ERR_CLASS_REDEFINED(name):
    return f"""Kooxda '{name}' horay ayaa loo dhisay!
    
        \033[1;31m koox {name} {{}}; koox {name} {{}}; \033[1;35m // Ma waxaad rabtaa inaad isku magac laba qof u bixisid?
        \033[1;32m // Isticmaal magac cusub ama ka saar qeexidda labaad."""

def ERR_VAR_REDEFINED(name):
    return f"""Keydiyaha '{name}' horay ayaa loogu qeexay meeshan.
    
        \033[1;31m keyd:tiro {name} = 1; keyd:eray {name} = "A"; \033[1;35m // Hal magac hal qof ayaa leh!
        \033[1;32m {name} = "B"; \033[1;35m // Haddii aad rabo inaad beddesho qiimaha, iska daa 'keyd' mar kale."""

def ERR_BREAK_OUTSIDE_LOOP():
    return f"""'joog' (break) waxaa la isticmaali karaa oo keliya gudaha wareeg (loop)!
    
        \033[1;31m joog; \033[1;35m // Xaggee ka joogsanaysaa adigoo aan xitaa socon?"""

def ERR_CONTINUE_OUTSIDE_LOOP():
    return f"""'kasoco' (continue) waxaa la isticmaali karaa oo keliya gudaha wareeg (loop)!
    
        \033[1;31m kasoco; \033[1;35m // Maxaad 'kasoconaysaa' adigoo aan tartankaba ku jirin?"""

def ERR_NOT_A_DICTIONARY_SIMPLE():
    return f"""Isku day inaad u isticmaasho wax sidii qaamuus (dictionary), laakiin maaha!
    
        \033[1;31m keyd:tiro x = 10; x["fure"]; \033[1;35m // 'tiro' ma laha wax fureyaal ah.
        \033[1;32m keyd:qaamuus q = {{ "x": 1 }}; q["x"]; \033[1;35m // Qaamuus dhab ah isticmaal."""

def ERR_INDEX_NOT_INT():
    return f"""'boos' (index) waa inuu ahaadaa 'tiro' (integer)!
    
        \033[1;31m tix["kow"] \033[1;35m // Ma waxaad moodday in tixdu ay tahay qaamuus? 
        \033[1;35m // Tixaha boosaskoodu waa lambar (0, 1, 2...).
        \033[1;32m tix[0] \033[1;35m // Isticmaal tiro markasta."""

# Simple fallbacks for internal compiler errors
def ERR_UNKNOWN_TYPE(type_name):
    return f"Nooca xogta '{type_name}' lama yaqaan. Hubi naxwahaaga!"

def ERR_ASSIGNMENT_NON_LVALUE_SIMPLE():
    return "Qiime lama gelin karo dhinaca bidix ee '='. Xisaabta baro sxb!"

def ERR_CONSTRUCTOR_ARG_TYPE_MISMATCH(index, class_name, expected, found):
    return f"Dhisaha '{class_name}' wuxuu qaybta {index} ka rabaa '{expected}', laakiin waxaad siisay '{found}'."

def ERR_METHOD_ARG_TYPE_MISMATCH(param_def, method_name, expected, found):
    return f"Hawsha '{method_name}' waxay qaybta {param_def} ka rabtaa '{expected}', laakiin waxaad siisay '{found}'."

def ERR_CLASS_INSTANTIATION_NOT_A_CLASS(name):
    return f"'{name}' ma ahan koox (class). Ma dhisid kartid wax aan koox ahayn!"

def ERR_ARG_TYPE_MISMATCH_SIMPLE(index, name, expected, found):
    return f"Hawsha '{name}' waxay qaybta {index} ka rabtaa '{expected}', laakiin waxaad siisay '{found}'."

def ERR_METHOD_NOT_FOUND_ON_ARRAY(method_name):
    return f"Tixda (array) ma laha hawl la yiraahdo '{method_name}'. Hubi hawlaha tixaha sida 'gali' iyo 'kasaar'."

def ERR_METHOD_NOT_FOUND_ON_STRING(method_name):
    return f"Erayga (string) ma laha hawl la yiraahdo '{method_name}'."

def ERR_GALI_BOOS_MISSING():
    return "Markaad 'gali' u isticmaalayso laba halbeeg, kan hore waa inuu ahaadaa 'boos = ...'."

def ERR_GALI_ARG_COUNT():
    return "Hawsha 'gali' waxay rabtaa 1 ama 2 halbeeg oo kaliya."

def ERR_KASAAR_ARG_COUNT():
    return "Hawsha 'kasaar' waxay rabtaa 1 halbeeg oo kaliya."

def ERR_RETURN_TYPE_MISMATCH(expected, found):
    return f"Hawsha waa inay soo celisaa '{expected}', laakiin waxaad ku dhex ooysaa '{found}'."

def ERR_NOT_AN_ARRAY_SIMPLE():
    return "Ma ahan tix (array). Ha isku dayin inaad boos ka gasho wax aan tix ahayn."

def ERR_NOT_A_CLASS(type_name):
    return f"'{type_name}' ma ahan koox (class). Ma laha xubno (members)."

def ERR_CLASS_NOT_FOUND(class_name):
    return f"Kooxda '{class_name}' lama helin. Ma adigaa iska dhisay magacaas?"

def ERR_NAMED_ARG_NOT_FOUND(name, context):
    return f"Hawsha '{context}' ma laha halbeeg magaciisu yahay '{name}'."

def ERR_NAMED_ARG_DUPLICATE(name, context):
    return f"Halbeegga '{name}' laba jeer ayaad siisay hawsha '{context}', sidee wax u wadaa?."

def ERR_ARG_MISSING(name, context):
    return f"Halbeegga '{name}' ayaa ka dhiman hawsha '{context}'. Maxaad uga tagtay isaga?"

def ERR_CLASS_NAME_NOT_CAPITAL(name):
    return f"""Magaca kooxda '{name}' waa inuu ku bilaawdaa xaraf weyn (Capital)!
    
        \033[1;31m koox {name} {{ ... }} \033[1;35m // Sidani waa khalad! Magacyada kooxaha waa in la weyneeyaa.
        \033[1;32m koox {name[0].upper() + name[1:] if len(name) > 1 else name.upper()} {{ ... }} \033[1;35m // Sidani waa naxwe sax ah."""

def ERR_FUNCTION_NAME_NOT_LOWERCASE(name):
    return f"""Magaca hawsha '{name}' waa inuu ku bilaawdaa xaraf yar (lowercase)!
    
        \033[1;31m hawl {name}() {{ ... }} \033[1;35m // Sidani waa khalad! Hawlaha ha ku bilaabin xaraf weyn.
        \033[1;32m hawl {name[0].lower() + name[1:] if len(name) > 1 else name.lower()}() {{ ... }} \033[1;35m // Sidani waa sax."""

def ERR_CANNOT_PRINT_TYPE(type_name):
    return f"""Noocan '{type_name}' ma ahan mid la 'qor' gareyn karo!
    
        \033[1;31m qor(shay_kooxeed) \033[1;35m // Sidani waa khalad! Kooxaha (classes) si toos ah looma qoro.
        \033[1;32m qor(shay.magac) \033[1;35m // Sidani waa sax. Qor xubnaha ka kooban kooxda (sida tiro ama eray)."""

def ERR_USE_AFTER_MOVE(var_name, move_node_info):
    return f"""Variable-ka '{var_name}' milkiyaddiisa waa la wareejiyay!

        \033[1;31m {var_name} ... \033[1;35m // Khalad! Variable-ku hadda ma haayo wax milkiyad ah.
        \033[1;32m // Mulkiyadiisa waxa uu ku wariijiyay heshiiskii ka dhacay: {move_node_info}
        \033[1;34m Talo: Haddii aad rabto inaad mar kale isticmaasho, samee nuqul (copy) ama ha wareejin."""

def ERR_UNINITIALIZED_VARIABLE(name):
    return f"""Keydiyaha '{name}' ma laha wax qiime ah (Uninitialized)! 

        \033[1;31m qor({name}); \033[1;35m // '{name}' booskiisii waa eber. Ma waxaad moodday inuu hawada ka dhalanayo?
        \033[1;32m {name} = 10; qor({name}); \033[1;35m // Horta qiime sii intaadan u yeerin!"""
# ============================================================================
# Missing Error Functions - Added to fix semantic analyzer crashes
# These 18 functions were being called but not defined in semantic_errors.py
# ============================================================================

def ERR_UNDEFINED_CLASS(class_name):
    return f"""Kooxda '{class_name}' lama helin!
    
        \033[1;31m koox {class_name} {{ ... }} \033[1;35m // Kooxdan ma jirto!
        \033[1;32m // Hubi inaad si sax ah u qortay magaca kooxda."""
        # Check if you defined this class somewhere

def ERR_ARRAY_TYPE_MISMATCH(expected_type, actual_type):
    return f"""Noocyada tixda (array) iskuma mid ahan!
    
        \033[1;31m tix:{expected_type} arr = [qiime_{actual_type}] \033[1;35m // Nooc kale oo tix ah ayaa la rabay!
        \033[1;32m tix:{expected_type} arr = [{expected_type}_qiime] \033[1;35m // Isticmaal tix isku nooc ah."""
        # Arrays must have consistent element types

def ERR_UNKNOWN_EXPR_TYPE(expr_type):
    return f"""Noocan yaaya ee soo-idato ma ahan mid la aqoonsan yahay: '{expr_type}'
    
        \033[1;31m // Qaybta code-kaani waxa ay soo generate-neyaa nooc aan la garanayn
        \033[1;35m // Hubi inaad isticmaalayno operations-ka sax ah."""
        # Contact the language maintainers if this persists

def ERR_CLASS_INHERITS_UNKNOWN(class_name, parent_name):
    return f"""Kooxda '{class_name}' waxay dhaxlayo '{parent_name}' oo aan jirin!
    
        \033[1;31m koox {class_name} dhaxlaya {parent_name} {{ ... }} \033[1;35m // Kooxda '{parent_name}' ma jirto!
        \033[1;32m koox {parent_name} {{ ... }} \033[1;35m // Horta qor kooxda '{parent_name}'."""
        # Define the parent class before inheriting

def ERR_INHERITANCE_CYCLE(class_name, parent_name):
    return f"""Cycle-ka inheritance ayaa jira! '{class_name}' waxay dhaxlayo '{parent_name}' oo ay ku noqonaysaa '{class_name}'!
    
        \033[1;31m koox A dhaxlaya B {{ ... }} \033[1;35m // Cycle: A -> B -> A
        \033[1;32m // Ka saar hal inheritance si cycle-ka laiska jaro."""
        # Remove one of the inheritance links

def ERR_NO_CONSTRUCTOR(class_name, arg_count):
    return f"""Kooxda '{class_name}' lama hayo dhis (constructor)!
    
        \033[1;31m keyd:{class_name} obj = {class_name}(); \033[1;35m // dhis() ma jiro!
        \033[1;32m koox {class_name} {{ dhis() {{ }} }} \033[1;35m // Ku dar dhis() si aad u dhistid shay."""
        # Add a constructor method to the class

def ERR_FUNCTION_REDEFINED(name, is_method=False):
    prefix = "shaqo" if is_method else "hawl"
    return f"""Hawl '{name}' horay ayaa loo qeexay!
    
        \033[1;31m {prefix} {name}() {{ ... }} \033[1;35m // Waxaa jira hal xulasho oo kan ah
        \033[1;32m // Bedel magaca mid ka mid ah ama ka saar mid."""
        # Rename or remove one of the duplicate functions

def ERR_DEFAULT_ARG_TYPE_MISMATCH(param_name, expected_type, actual_type):
    return f"""Qiimaha default-ka ee '{param_name}' waa khaldan!
    
        \033[1;31m hawl test({param_name}:{expected_type} = qiime_{actual_type}) \033[1;35m // Type-ka waa khaldan
        \033[1;32m hawl test({param_name}:{expected_type} = {expected_type}_qiime) \033[1;35m // Isticmaal qiime isku nooc ah."""
        # Default value must match parameter type

def ERR_DEFAULT_ARG_ORDER():
    return f"""Default arguments waa inay had iyo jeer u dambeeyaan arguments-ka regular!
    
        \033[1;31m hawl test(x:tiro, y:tiro=5, z:tiro) \033[1;35m // z waa regular, ka dib y oo default!
        \033[1;32m hawl test(x:tiro, z:tiro, y:tiro=5) \033[1;35m // Default-ka wuxuu weynaa regular."""
        # Put required params before optional params

def ERR_CANNOT_CALL_ON_OBJECT(method_name, object_type):
    return f"""'{object_type}' waa shay, lama yeeli karo '{method_name}()'!
    
        \033[1;31m shay.{method_name}() \033[1;35m // '{object_type}' waa shay, lama yeeli karo
        \033[1;32m shay.x \033[1;35m // isticmaal xubnaha keliya."""
        # Only objects (classes) have methods

def ERR_BUILTIN_NAMED_ARG(func_name):
    return f"""Built-in function '{func_name}' ma aqbato named arguments!
    
        \033[1;31m {func_name}(magac = "qiime") \033[1;35m // Sidani waa khalad!
        \033[1;32m {func_name}(qiime) \033[1;35m // Isticmaal positional arguments keliya."""
        # Don't use named arguments for built-in functions

def ERR_FUNCTION_VAR_NAMED_ARGS():
    return f"""Functions-ka (not methods) ma aqbato named arguments!
    
        \033[1;31m hawl test(x:tiro, y:tiro) {{}} test(x=1, y=2) \033[1;35m // Sidani waa khalad!
        \033[1;32m test(1, 2) \033[1;35m // Isticmaal positional arguments."""
        # Use positional arguments for functions

def ERR_ARG_COUNT_MISMATCH(func_name, expected_count, actual_count):
    return f"""Tirada arguments-ka waa khaldan! '{func_name}' waxay rabtaa {expected_count}, laakiin waxaad siisay {actual_count}.
    
        \033[1;31m {func_name}(arg1, arg2, arg3) \033[1;35m // {actual_count} argument, laakiin {expected_count} ayaa la rabay
        \033[1;32m {func_name}({', '.join([f'arg{i+1}' for i in range(expected_count)])}) \033[1;35m // {expected_count} argument."""
        # Check the function definition

def ERR_DICT_KEY_NOT_STRING(key_type):
    return f"""Qaamuus (dictionary) key waa inuu ahaadaa eray (string)!
    
        \033[1;31m qaamuus[{key_type}_qiime] = "value" \033[1;35m // Keys waa inuu noqoto eray!
        \033[1;32m qaamuus["key"] = "value" \033[1;35m // Isticmaal string ah oo key ahaan."""
        # Dictionary keys must be strings

def ERR_DICT_ACCESS_NON_DICT(var_name):
    return f"""'{var_name}' waa qaamuus (dictionary), la awoodaa in la galo!
    
        \033[1;31m {var_name}[key] \033[1;35m // '{var_name}' ma ahan qaamuus!
        \033[1;32m // Hubi in '{var_name}' uu yahay qaamuus ama isticmaal tix/wax."""
        # Check the variable type

def ERR_FOR_RANGE_NOT_INT(start_type, end_type):
    return f"""Xaqiiqada xukusho (for loop) waxay rabtaa tiro (tiro)门外, laakiin '{start_type}' iyo '{end_type}' ayaa la siiyay!
    
        \033[1;31m xukusho i = {start_type}_qiime; i < {end_type}_qiime; i++ \033[1;35m // Tiroood waa khaldan!
        \033[1;32m xukusho i:tiro = 0; i < 10; i++ \033[1;35m // Isticmaal tiro keliya."""
        # Use integers (tiro) for loop range

def ERR_FOR_EACH_NOT_ITERABLE(iterable_type):
    return f"""Xukusho kasta (for-each) waxay rabtaa tix (array)门外, laakiin '{iterable_type}' ayaa la siiyay!
    
        \033[1;31m xukusho (x : {iterable_type}_qiime) {{ }} \033[1;35m // Waa khaldan!
        \033[1;32m xukusho (x : tix_kan) {{ }} \033[1;35m // Isticmaal tix (array)."""
        # Use arrays for iteration

def ERR_BINARY_OP_TYPE_MISMATCH(left_type, right_type, op):
    return f"""Noocyada xogta iskuma mid ahan (Type Mismatch) ee Binary Operation!

        \033[1;31m qiime left: {left_type} \033[0m {op} \033[1;31m qiime right: {right_type} \033[0m

        \033[1;35m// Isticmaal nooco isku mid ah."""
        # Arithmetic operations require compatible numeric types

def ERR_ASSIGNMENT_NON_LVALUE():
    return f"""Qiime lama gelin karo dhinaca bidix ee calaamadda '='!

        \033[1;31m x + 1 = 5 \033[1;35m // 'x + 1' waa expression, lama yeeli karo assignment
        \033[1;32m x = 5 \033[1;35m // 'x' keliya ayaa la gelin karaa."""
