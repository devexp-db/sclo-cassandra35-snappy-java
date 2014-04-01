Name:             snappy-java
Version:          1.0.4.1
Release:          8%{?dist}
Summary:          Fast compressor/decompresser
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://code.google.com/p/snappy-java

# hg clone --insecure -r snappy-java-1.0.4.1 https://code.google.com/p/snappy-java/
# cd snappy-java && hg archive -p snappy-java-1.0.4.1/ -X 'lib/*.jar' -t tgz ../snappy-java-1.0.4.1-CLEAN.tgz
Source0:          snappy-java-%{version}-CLEAN.tgz

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    mvn(org.apache.felix:org.osgi.core)

%description
A Java port of the snappy, a fast compresser/decompresser written in C++.

%package javadoc
Summary:          Javadoc for %{name}
BuildArch:        noarch

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%pom_remove_dep org.osgi:core
%pom_add_dep org.apache.felix:org.osgi.core:1.4.0:provided
%pom_xpath_remove "pom:project/pom:dependencies/pom:dependency[pom:scope = 'test' ]"
%pom_xpath_remove "pom:build/pom:extensions"

# Unwanted
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-source-plugin

chmod 644 NOTICE README
sed -i 's/\r//' LICENSE NOTICE README

%build
# no xerial package available
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE README

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Mar 31 2014 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.4.1-8
- Switch to XMvn
- Use pom macros

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.4.1-7
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.4.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 4 2012 Ricardo Arguello <ricardo@fedoraproject.org> - 1.0.4.1-2
- Cleanup of the spec file

* Tue Feb 21 2012 Marek Goldmann <mgoldman@redhat.com> - 1.0.4.1-1
- Initial packaging
