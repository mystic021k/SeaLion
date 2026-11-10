function configureAccountTypeOptions() {
  let accountTypeGroup = document.getElementById("acctyperadio");
  let mailAccount = document.getElementById("mailaccount");
  let newsAccount = document.getElementById("newsaccount");

  if (!accountTypeGroup || !mailAccount || !newsAccount) {
    Components.utils.reportError("Could not find account type radio buttons.");
    return;
  }

  accountTypeGroup.insertBefore(mailAccount, newsAccount);

  let ispBox = document.getElementById("ispBox");
  if (ispBox) {
    let hasProvider = false;
    for (let child = ispBox.firstElementChild; child; child = child.nextElementSibling) {
      if (child.localName == "radio") {
        hasProvider = true;
        break;
      }
    }
    ispBox.hidden = !hasProvider;
  }

  let requestedType = window.arguments && window.arguments[0] &&
                      window.arguments[0].acctType;
  let selectedItemId = requestedType == "newsgroups" ? "newsaccount" :
                       requestedType == "movemail" ? "Movemail" : "mailaccount";
  let selectedItem = document.getElementById(selectedItemId);
  if (selectedItem)
    accountTypeGroup.selectedItem = selectedItem;

  if (requestedType == "mail") {
    let accountWizard = document.getElementById("AccountWizard");
    if (accountWizard)
      accountWizard.advance("identitypage");
  }
}

window.addEventListener("load", function() {
  window.setTimeout(configureAccountTypeOptions, 0);
}, false);
