int CFootBotDiffusion::cStratego(bool within, float angle, float prox, float limit){
   string mystring="./uppaalStratego/callStratego ";
   string controllerName = "uppaalStratego/controller0.xml";
   string queryName = "uppaalStratego/query.q";
   string withinString;
   if(within) withinString="true";
   else withinString="false";

   std::ostringstream buffangle;
   buffangle<<angle;
   std::ostringstream buffprox;
   buffprox<<prox;
   std::ostringstream bufflimit;
   bufflimit<<limit;

   mystring = mystring + withinString + " " + buffangle.str() + " " + buffprox.str() + " " + bufflimit.str() + " " + controllerName + " " + queryName; 
   cout<<mystring<<endl;
   string action;
   FILE* stream;
   const int max_buffer = 256;
   char buffer[max_buffer];
   mystring.append(" 2>&1");
   stream = popen(mystring.c_str(), "r");
   if (stream) {
   while (!feof(stream))
   if (fgets(buffer, max_buffer, stream) != NULL) action.append(buffer);
   //cout<<"action: "<<action<<endl;
   pclose(stream);
   }
   return stoi(action);
}
